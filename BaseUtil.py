import re
from urllib.parse import urlparse
import json
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

from Util import Util
from cookie_test import fetch_chrome_cookie


class BaseUtil(Util):
    def __init__(self, username, passwd, adminid='15870', factoryid='1', baseurl='https://crm.konka.com',
                 bjdomain='http://north.bangjia.me'):
        parsed_uri = urlparse(baseurl)
        self.host = parsed_uri.netloc
        self.username = username
        self.passwd = passwd
        self.baseurl = baseurl
        self.adminid = adminid
        self.factoryid = factoryid
        self.bjdomain = bjdomain
        self.mainurl = self.baseurl + '/admin/page!main.action'
        self.searchurl = self.baseurl + '/afterservice/afterservice!api.action'
        self.session = requests.Session()
        self.agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        self.datasuccess = {'code': 1, 'msg': '抓单成功', 'element': ''}
        self.datafail = {'code': 0, 'msg': '抓单失败,请确认账号密码是否正确'}
        self.dataverify = {'code': 2, 'msg': '登录过期，请重新登录', 'element': ''}
        self.headers = {'Content-Type': 'application/json;charset=UTF-8',
                        'User-Agent': self.agent, 'Referer': self.baseurl,
                        'Upgrade-Insecure-Requests': '1', 'Host': self.host, 'Origin': self.baseurl,
                        'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Accept': 'application/json, text/plain, */*'}
        self.initCookie()

    def getsoup(self, response):
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, features="lxml")

    def parseHtml(self, htmlstr):
        bsObj = BeautifulSoup(htmlstr, features="lxml")
        if not bsObj:
            return ""
        return bsObj.text.strip()

    def getjson(self, response):
        response.encoding = 'utf-8'
        try:
            result = json.loads(response.text)
        except Exception as e:
            print("getjson failed:{}".format(str(e)))
            result = None
        return result

    @staticmethod
    def merge(lst1, lst2, keys, isCover=False):
        def generate_key(item):
            if type(keys) == list:
                return "_".join(str(v) for k, v in item.items() if k in keys)
            else:
                return "_".join(str(v) for k, v in item.items() if k == keys)

        hash_map = {}
        for item in lst1 + lst2:
            if isCover:
                hash_map[generate_key(item)] = item
            else:
                hash_map.setdefault(generate_key(item), item)
        result = list(hash_map.values())
        return result if result else []

    def initCookie(self, cookies=None):
        pass

    def login(self, param=None):
        pass

    def loadOrders(self, param=None):
        pass

    @staticmethod
    def getCookie(domains=[], isExact=False):
        return fetch_chrome_cookie(domains, isExact=isExact)

    @staticmethod
    def getCookies(cookie):
        cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
        return cookies

    @staticmethod
    def merge(lst1, lst2, keys, isCover=False):
        def generate_key(item):
            if type(keys) == list:
                return "_".join(str(v) for k, v in item.items() if k in keys)
            else:
                return "_".join(str(v) for k, v in item.items() if k == keys)

        hash_map = {}
        for item in lst1 + lst2:
            if isCover:
                hash_map[generate_key(item)] = item
            else:
                hash_map.setdefault(generate_key(item), item)
        result = list(hash_map.values())
        return result if result else []

    @staticmethod
    def getDateBefore(day):
        return (date.today() - timedelta(days=day)).strftime("%Y-%m-%d")

    @staticmethod
    def clearKey(data, datakey, destkey='address'):
        if datakey in data and data[destkey] and data[destkey].strip().startswith(data[datakey].strip()):
            data[destkey] = data[destkey].replace(data[datakey], '', 1).strip()
        return data

    @staticmethod
    def clearAddress(orderinfo, destkey='address'):
        if destkey not in orderinfo:
            return orderinfo
        orderinfo = BaseUtil.clearKey(orderinfo, "province", destkey)
        orderinfo = BaseUtil.clearKey(orderinfo, "city", destkey)
        orderinfo = BaseUtil.clearKey(orderinfo, "county", destkey)
        orderinfo = BaseUtil.clearKey(orderinfo, "town", destkey)
        return orderinfo

    @staticmethod
    def getTimeStr(string, isDefault=True):
        defaultValue = '00:00:00' if isDefault else ''
        try:
            time_str = re.compile(r"\d{2}:\d{1,2}").findall(string)[0]
            result = time_str if BaseUtil.isTime(time_str) else defaultValue
            return result
        except IndexError:
            return defaultValue

    @staticmethod
    def isTime(time_str):
        return BaseUtil.isTimesecondstr(time_str) or BaseUtil.isTimestr(time_str)

    @staticmethod
    def isTimesecondstr(time_str):
        try:
            datetime.strptime(time_str, '%H:%M:%S')
            return True
        except ValueError:
            return False

    @staticmethod
    def isTimestr(time_str):
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False

    @staticmethod
    def isDatetimestr(datetime_str):
        try:
            datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False

# print("getDateBefore(0)={}".format(BaseUtil.getDateBefore(0)))
