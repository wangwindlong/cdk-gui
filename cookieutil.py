import browsercookie
import requests
from bs4 import BeautifulSoup

# 获取cookie，前提是需要浏览器登陆过
# chrome_cookie = browsercookie.chrome()
# for cookie in chrome_cookie:
#     print(cookie)


# -*- coding=utf-8 -*-
import os
import json
import base64
import sqlite3
import win32crypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def GetString(LocalState):
    with open(LocalState, 'r', encoding='utf-8') as f:
        s = json.load(f)['os_crypt']['encrypted_key']
    return s


def pull_the_key(base64_encrypted_key):
    encrypted_key_with_header = base64.b64decode(base64_encrypted_key)
    encrypted_key = encrypted_key_with_header[5:]
    key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key


def DecryptString(key, data):
    nonce, cipherbytes = data[3:15], data[15:]
    aesgcm = AESGCM(key)
    plainbytes = aesgcm.decrypt(nonce, cipherbytes, None)
    plaintext = plainbytes.decode('utf-8')
    return plaintext


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

NONCE_BYTE_SIZE = 12


def encrypt(cipher, plaintext, nonce):
    cipher.mode = modes.GCM(nonce)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return (cipher, ciphertext, nonce)


def decrypt(cipher, ciphertext, nonce):
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)


def get_cipher(key):
    cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
    return cipher



if __name__ == '__main__':
    # HOMEPATH  LOCALAPPDATA
    LocalState = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Local State'
    Cookies = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Default\Cookies'
    print(Cookies)
    con = sqlite3.connect(Cookies)
    res = con.execute('select encrypted_value from cookies').fetchall()
    con.close()

    key = pull_the_key(GetString(LocalState))
    for i in res:
        print(DecryptString(key, i[0]))

    input('ok')
