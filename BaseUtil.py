import re
from urllib.parse import urlparse
import json
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime


class BaseUtil:
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
        self.agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/81.0.4044.113 Safari/537.36'
        self.datasuccess = {'code': 1, 'msg': '抓单成功', 'element': ''}
        self.datafail = {'code': 0, 'msg': '抓单失败,请确认账号密码是否正确'}
        self.headers = {'Content-Type': 'application/json;charset=UTF-8',
                        'User-Agent': self.agent,
                        'Upgrade-Insecure-Requests': '1', 'Host': self.host, 'Origin': self.baseurl,
                        'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Accept': 'application/json, text/plain, */*'}

    def getsoup(self, response):
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, features="lxml")

    def login(self, param=None):
        pass

    def loadOrders(self, param=None):
        pass

    @staticmethod
    def getCookies(cookie):
        try:
            s = cookie.split("; ")
            cookies = {}
            for c in s:
                content = c.split("=")
                if len(content) > 1:
                    cookies[content[0]] = content[1]
            return cookies
        except Exception as e:
            print("getCookies", e)
            return ""

    @staticmethod
    def getDateBefore(day):
        return (date.today() - timedelta(days=day)).strftime("%Y-%m-%d")

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
