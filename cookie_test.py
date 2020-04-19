import os
import sys
import sqlite3
import http.cookiejar as cookiejar
import json, base64
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
    if sys.platform.startswith('linux'):
        password = 'peanuts'
        iterations = 1
    else:
        raise NotImplementedError

    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2

    salt = 'saltysalt'
    iv = ' ' * 16
    length = 16
    key = PBKDF2(password, salt, length, iterations)
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    decrypted = cipher.decrypt(encrypted[3:])
    return decrypted[:-ord(decrypted[-1])]


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
        try:
            return unix_decrypt(encrypted_txt)
        except NotImplementedError:
            return None


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


def existInDomain(domain, cookie):
    if domain['domain'] == cookie['host']:
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


def existInArray(domains, cookie):
    if not domains:
        return True
    for domain in domains:
        if existInDomain(domain, cookie):
            return True
    return False


def fetch_chrome_cookie(domains):
    try:
        jar = ChromeCookieJar()
        jar.load()
        cookieValue = ''
        for item in jar.cookies:
            if existInArray(domains, item):
                cookieValue += item['name'] + '=' + item['value'] + '; '
        return cookieValue[:-1]
    except Exception as e:
        print("fetch_chrome_cookie",e)
        return ""

if __name__ == '__main__':
    print(fetch_chrome_cookie(
        [{"domain": ".xiaomi.com", "fields": ["mstz", "xst",'uLocale']},
         {"domain": ".be.xiaomi.com", "fields": ["mstz", "xst",'uLocale']},
         {"domain": "xms.be.xiaomi.com"},
         {"domain": ".xms.be.xiaomi.com"},
         {"domain": ".account.xiaomi.com"},
         {"domain": ".mi.com"}]))
    # print(fetch_chrome_cookie(['xiaomi.com']))
