import os
import sqlite3
from collections import defaultdict
from win32.win32crypt import CryptUnprotectData

'''
实际使用场景请自行修改Cookies/cookies.sqlite位置，下面代码均为默认安装的位置，有些绿色版的文件夹位置以及老版本的渗透版火狐浏览器位置需要自行修改
'''


# 获取chrome浏览器的cookies
def getcookiefromchrome():
    cookiepath = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    sql = "select host_key,name,encrypted_value from cookies"
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        select_cookie = (cu.execute(sql).fetchall())
        cookie_list = []
        for host_key, name, encrypted_value in select_cookie:
            cookie = CryptUnprotectData(encrypted_value)[1].decode()
            cookies = {host_key: name + ":" + cookie}
            cookie_list.append(cookies)
        d = defaultdict(list)
        for cookie_item in cookie_list:
            for key, value in cookie_item.items():
                d[key].append(value.strip())
        print(dict(d))


getcookiefromchrome()
