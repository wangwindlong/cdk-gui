import os
import json
import base64
import win32crypt
from Crypto.Cipher import AES
import sqlite3

'''
[(0, 'creation_utc', 'INTEGER', 1, None, 0), (1, 'host_key', 'TEXT', 1, None, 0), (2, 'name', 'TEXT', 1, None, 0), (3, 'value', '
TEXT', 1, None, 0), (4, 'path', 'TEXT', 1, None, 0), (5, 'expires_utc', 'INTEGER', 1, None, 0), (6, 'is_secure', 'INTEGER', 1, No
ne, 0), (7, 'is_httponly', 'INTEGER', 1, None, 0), (8, 'last_access_utc', 'INTEGER', 1, None, 0), (9, 'has_expires', 'INTEGER', 1
, '1', 0), (10, 'is_persistent', 'INTEGER', 1, '1', 0), (11, 'priority', 'INTEGER', 1, '1', 0), (12, 'encrypted_value', 'BLOB', 0
, "''", 0), (13, 'samesite', 'INTEGER', 1, '-1', 0), (14, 'source_scheme', 'INTEGER', 1, '0', 0)]
'''
sql = """
SELECT
    host_key, name, path,encrypted_value as value
FROM
    cookies
"""


def get_decrypted_key():
    path = r'%LocalAppData%\Google\Chrome\User Data\Local State'
    path = os.path.expandvars(path)
    with open(path, 'r', encoding='utf8') as file:
        encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
    encrypted_key = base64.b64decode(encrypted_key)  # Base64 decoding
    encrypted_key = encrypted_key[5:]  # Remove DPAPI
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]  # Decrypt key
    # print("decrypt",decrypted_key)
    return decrypted_key


# get cookie
def get_chrome_cookie():
    cookies_path = os.environ['HOMEPATH'] + r'\AppData\Local\Google\Chrome\User Data\Default\Cookies'
    cookies_path = os.path.join(os.environ['LOCALAPPDATA'], os.environ['HOMEPATH'], cookies_path)
    con = sqlite3.connect(cookies_path)
    res = con.execute(sql).fetchall()
    # names = con.execute('PRAGMA  table_info([cookies])').fetchall()
    # print(names)
    con.close()
    # print(res)
    return res


def decrypt_chrome_cookie(decrypted_key, data):
    # data = bytes.fromhex('763130...') # the encrypted cookie
    if data[:3] == b'v10':
        nonce = data[3:3 + 12]
        ciphertext = data[3 + 12:-16]
        tag = data[-16:]
        cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=nonce)
        # plaintext = cipher.decrypt_and_verify(ciphertext, tag) # the decrypted cookie
        plaintext = cipher.decrypt(ciphertext)
        # print(plaintext)
        return plaintext
    else:
        # print('old cookie none decrypt')
        return ""


def fetch_chrome_cookies(domain=''):
    res = get_chrome_cookie()
    list = []
    for i in res:
        if domain in i[0]:
            item = {}
            # print(type(i[3]),i[3])
            data = i[3]  # the encrypted cookie
            key = get_decrypted_key()
            plaintext = decrypt_chrome_cookie(key, data)
            plaintext = str(plaintext, encoding="utf-8")
            # print("host:", i[0], "name:", i[1], "path:", i[2], "value:", plaintext)
            item["host"] = i[0]
            item["name"] = i[1]
            item["path"] = i[2]
            item["value"] = plaintext
            list.append(item)
    return list


def fetch_chrome_cookie(domain=''):
    cookie_list = fetch_chrome_cookies(domain)
    cookieValue = ''
    for item in cookie_list:
        cookieValue += item['name'] + '=' + item['value'] + '; '
    # print("fetch_chrome_cookie:" + cookieValue)
    return cookieValue[:-1]


if __name__ == '__main__':
    print(fetch_chrome_cookie('xiaomi.com'))
