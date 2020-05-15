from urllib.parse import urlparse
import json
import requests


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

    def login(self, param=None):
        pass

    def loadOrders(self, param=None):
        pass
