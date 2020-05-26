import os
import sys
import sqlite3
import http.cookiejar as cookiejar
import json, base64

import requests

import aesgcm

sql = """
SELECT
    host_key, name, path,encrypted_value as value
FROM
    cookies
"""


def dpapi_decrypt(encrypted):
    import ctypes
    import ctypes.wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]

    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result


def unix_decrypt(encrypted):
    if not encrypted or len(encrypted) <= 3:
        return None
    print("unix_decrypt encrypted={}".format(encrypted))
    if sys.platform.startswith('linux'):
        password = 'peanuts'.encode('utf8')
        iterations = 1
    else:
        raise NotImplementedError

    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2

    salt = b'saltysalt'
    iv = b' ' * 16
    length = 16
    key = PBKDF2(password, salt, length, iterations)
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    decrypted = cipher.decrypt(encrypted[3:])
    print("unix_decrypt decrypted={}".format(decrypted))
    # return decrypted[:-ord(decrypted[-1])]
    return decrypted[:-decrypted[-1]]


def get_key_from_local_state():
    jsn = None
    with open(os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Local State"), encoding='utf-8',
              mode="r") as f:
        jsn = json.loads(str(f.readline()))
    return jsn["os_crypt"]["encrypted_key"]


def aes_decrypt(encrypted_txt):
    encoded_key = get_key_from_local_state()
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = dpapi_decrypt(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = aesgcm.get_cipher(key)
    return aesgcm.decrypt(cipher, encrypted_txt[15:], nonce)


def chrome_decrypt(encrypted_txt):
    if sys.platform == 'win32':
        try:
            if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                decrypted_txt = dpapi_decrypt(encrypted_txt)
                return decrypted_txt.decode()
            elif encrypted_txt[:3] == b'v10':
                decrypted_txt = aes_decrypt(encrypted_txt)
                return decrypted_txt[:-16].decode()
        except WindowsError:
            return None
    else:
        return unix_decrypt(encrypted_txt)
        # try:
        #
        # except NotImplementedError:
        #     return None


def to_epoch(chrome_ts):
    if chrome_ts:
        return chrome_ts - 11644473600 * 000 * 1000
    else:
        return None


class ChromeCookieJar(cookiejar.FileCookieJar):
    def __init__(self, filename=None, delayload=False, policy=None):
        self.cookies = []
        if filename is None:
            if sys.platform == 'win32':
                filename = os.path.join(
                    os.environ['USERPROFILE'],
                    r'AppData\Local\Google\Chrome\User Data\default\Cookies')
                '''
                AppData\\Local\\Google\\Chrome\\User Data\\Profile [n]\\Cookies
                '''
            elif sys.platform.startswith('linux'):
                filename = os.path.expanduser(
                    '~/.config/google-chrome/Default/Cookies')
                if not os.path.exists(filename):
                    filename = os.path.expanduser(
                        '~/.config/chromium/Default/Cookies')
            if not os.path.exists(filename):
                filename = None
        cookiejar.FileCookieJar.__init__(self, filename, delayload, policy)

    def _really_load(self, f, filename, ignore_discard, ignore_expires):
        con = sqlite3.connect(filename)
        con.row_factory = sqlite3.Row
        con.create_function('decrypt', 1, chrome_decrypt)
        con.create_function('to_epoch', 1, to_epoch)
        cur = con.cursor()
        cur.execute(sql)
        for row in cur:
            if row['value'] is not None:
                name = row['name']
                value = chrome_decrypt(row['value'])
                host = row['host_key']
                path = row['path']
                cookie = {"name": name, "value": value, "host": host, "path": path}
                self.cookies.append(cookie)
                # print("host:" + str(host) + " path:" + str(path) + " name:" + str(name) + " value:" + str(value))
        cur.close()


def isDesiredDomain(origin, dest, isExact=True):
    if not isExact:
        return dest in origin
    else:
        return origin == dest


def existInDomain(domain, cookie, isExact=True):
    if isDesiredDomain(cookie['host'], domain['domain'], isExact):
        if "fields" in domain and domain["fields"] and len(domain['fields']) > 0:
            for field in domain['fields']:
                if field == cookie['name']:
                    return True
        else:
            return True
        if "filters" in domain and domain["filters"] and len(domain['filters']) > 0:
            for filter_item in domain['filters']:
                if filter_item == cookie['name']:
                    return False
            return True
        else:
            return True
    return False


def existInArray(domains, cookie, isExact=True):
    if not domains:
        return True
    for domain in domains:
        if existInDomain(domain, cookie, isExact):
            return True
    return False


def fetch_chrome_cookie(domains=[], isExact=True):
    try:
        jar = ChromeCookieJar()
        jar.load()
        cookieValue = ''
        for item in jar.cookies:
            if existInArray(domains, item, isExact):
                cookieValue += item['name'] + '=' + item['value'] + '; '
        return cookieValue[:-2]
    except Exception as e:
        print("fetch_chrome_cookie", e)
        return ""


if __name__ == '__main__':
    coo = fetch_chrome_cookie([{"domain": ".jd.com"}], False)
    print(coo)
    session = requests.Session()
    cookie = coo
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
               'Host': 'jdfw.jd.com', 'Origin': 'http://jdfw.jd.com', 'Accept-Encoding': 'gzip, deflate',
               'Cookie': cookie, 'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive',
               'Accept': 'application/json, text/javascript, */*; q=0.01', "X-Requested-With": "XMLHttpRequest",
               'Referer': 'http://jdfw.jd.com/receipt/receiptDashboardIndex?homePageDistinguish=notAppointed&serviceType=0'}
    data = {
        "esSwitch": "1", "subCompanyId": "10", "wareInfoId": "lw_10_334%%603_2", "outletsId": "0755860394",
        "sortKind": "4", "page": "1", "rows": "20", "sort": "returnTime", "order": "desc", "serviceType": "0",
        "fastDealNum": "5"
    }
    result = ""
    for item in data:
        result += item + "=" + data[item] + "&"
    result = result + "freeinstall=&startStatus=&endStatus=&timeout=&todayOtherReservationConditionName=&productBrand=&productType1=&productType2=&productType3=&orderId=&bizOrderId=&ordernoGroup=&customerName=&customerPhone=&serviceStreet=&wareId=&productName=&orderStatus=&orderStatusGroup=&createOrderTimeBegin=&createOrderTimeEnd=&reservationDateBegin=&reservationDateEnd=&firstReservationTimeBegin=&firstReservationTimeEnd=&changedReservationDateBegin=&changedReservationDateEnd=&feedbackStatus=&orderOrderStatus=&expectAtHomeDateBegin=&expectAtHomeDateEnd=&atHomeFinishDateBegin=&atHomeFinishDateEnd=&deliveryDateStart=&deliveryDateEnd=&homePageDistinguish=&fastDealNumByColor=&reservationStatus=&reportLessFlag=&superExperienceStore=&sourceOrderIdGroup=&sellerId=&sellerName=&eclpBusinessNo=&isFast="
    print(result)
    params = {}
    datas = result.split("&")
    for data in datas:
        content = data.split("=")
        if len(content) > 1:
            params[content[0]] = content[1]

    response = session.post("http://jdfw.jd.com/receipt/query.json", headers=headers, data=params)
    print(response.text)
