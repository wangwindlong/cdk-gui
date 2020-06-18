import json
from datetime import date, timedelta
from urllib.parse import urlparse, urlencode

import requests
from bs4 import BeautifulSoup

from Util import Util


class GreeUtil(Util):
    # def __init__(self, username, passwd, adminid='15870', factoryid='1', baseurl='http://pgxt.gree.com:7909',
    def __init__(self, username, passwd, adminid='15870', factoryid='1', baseurl='http://116.6.118.169:7909/hjzx/',
                 bjdomain='http://north.bangjia.me'):
        parsed_uri = urlparse(baseurl)
        self.host = parsed_uri.netloc
        self.username = username
        self.passwd = passwd
        self.baseurl = baseurl
        self.adminid = adminid
        self.factoryid = factoryid
        self.bjdomain = bjdomain
        self.loginurl = self.baseurl + "loginAction_login"
        self.mainurl = self.loginurl
        self.searchurl = self.baseurl + '/afterservice/afterservice!api.action'
        self.session = requests.Session()
        self.agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/81.0.4044.113 Safari/537.36'
        self.datasuccess = {'code': 1, 'msg': '抓单成功', 'element': ''}
        self.datafail = {'code': 0, 'msg': '抓单失败,请确认账号密码是否正确'}
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded',
                        'User-Agent': self.agent,
                        'Upgrade-Insecure-Requests': '1', 'Host': self.host, 'Referer': self.baseurl,
                        'Origin': parsed_uri.scheme + "://" + parsed_uri.netloc,
                        'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,'
                                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    def isLogin(self):
        response = self.session.get(self.loginurl, headers=self.headers)
        response.encoding = 'utf-8'
        # print(response.status_code)
        # print("isLogin response={}".format(response.text))
        return "新派工系统--&gt;主界面" in response.text

    def login(self):
        data = {"usid": self.username, "pswd": self.passwd, "loginflag": "loginflag"}
        response = self.session.post(self.loginurl, headers=self.headers, data=urlencode(data))
        response.encoding = 'utf-8'
        # print("login result={}".format(response.text))
        if response.status_code == 200:
            return "新派工系统--&gt;主界面" in response.text
        return False

    def loadMain(self):
        if not self.isLogin() and not self.login():
            return self.datafail
        headers = self.headers.copy()
        headers['Referer'] = self.baseurl + 'menu.jsp'
        # 加载安装工单查询
        url = self.baseurl + "az/doListLcLsAz?otype=az&xsorsh=1&cd=pgcx"
        response = self.session.get(url, headers=headers)
        # response.encoding = 'utf-8'
        # print("loadMain response={}".format(response))
        if response.status_code != 200:
            return self.datafail
        return list(self.search(url))
        # try:
        #     data = {"data": json.dumps(list(self.search(url)))}
        #     requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
        # except Exception as e:
        #     print("addorder failed:", e)
        #     return self.datafail
        # return self.datasuccess

    def search(self, url, page=1, totalcount=0, pagesize=50):
        headers = self.headers.copy()
        headers['Referer'] = url
        today = date.today()
        data = {"otype": "az", "xsorsh": "1", "cd": "pgcx", "s_azAssign.s_spid": "102",  # 商用空调
                "s_azAssign.s_cjdt_from": (today - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                "s_azAssign.s_cjdt_to": (today + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                "isFirstPage": "true" if page == 1 else "false", "paged": str(page)
                }
        response = self.session.post(self.baseurl + "az/doListLcLsAz", headers=headers, data=urlencode(data))
        bsObj = self.getsoup(response)
        totalcount = int(bsObj.find("span", {"id": "totalRecord"}).text.strip())
        print("search totalcount={}".format(totalcount))
        # isall = (page + 1) * pagesize >= totalcount
        isall = True
        tbody = bsObj.find("table", {"id": "tbody"}).find("tbody")
        if isall:
            yield from self.parseOrders(tbody.find_all("tr"))
        else:
            yield from self.parseOrders(tbody.find_all("tr"))
            yield from self.search(url, page + 1, totalcount, pagesize)

    def parseOrders(self, trlist):
        for tr in trlist:
            tablecolumns = tr.find_all("td")
            if tr and len(tablecolumns) > 2:
                data = self.parseorder(tablecolumns)
                detailUrl = self.baseurl + "az/" + tablecolumns[0].find("a")['href']
                if data:
                    data = self.orderdetail(data, detailUrl)
                    # print("parseorder data={}".format(data))
                    yield data

    def parseorder(self, tablecolumns):
        try:
            data = {}
            data['factorynumber'] = tablecolumns[2].text.strip()
            data['username'] = tablecolumns[4].text.strip()
            data['mobile'] = tablecolumns[5].text.strip()
            data['address'] = tablecolumns[6].text.strip()
            data['createname'] = tablecolumns[8].text.strip()
            data['ordertime'] = tablecolumns[9].text.strip()  # 创建时间
            data['companyid'] = self.factoryid
            data['machinebrand'] = "格力"
            data['machinetype'] = "商用空调"
            data['orgname'] = tablecolumns[10].text.strip()
            data['note'] = tablecolumns[12].text.strip()
            data['adminid'] = self.adminid
            data['description'] = "当前处理网点：{}，处理结果跟踪：{}，备注：{}".format(
                tablecolumns[10].text.strip(), tablecolumns[11].text.strip(), tablecolumns[12].text.strip())  # 具体描述
            return data
        except Exception as e:
            print("parseorder exception", e)
        return None

    def orderdetail(self, data, detailUrl):
        headers = self.headers.copy()
        headers['Referer'] = self.baseurl + "az/doListLcLsAz"
        # 加载安装工单查询
        response = self.session.get(detailUrl, headers=headers)
        response.encoding = 'utf-8'
        # print(response.url)
        # print("orderdetail response={}".format(response.text))
        if response.status_code != 200:
            return data
        bsObj = self.getsoup(response)
        # data['mastername'] = tablecolumns[10].text.strip()  # 师傅姓名 无法获取
        # data['mastermobile'] = tablecolumns[10].text.strip()  # 师傅电话 无法获取
        data['machineversion'] = str(bsObj.find("input", {"id": "jxid0"})["value"])
        data['buydate'] = str(bsObj.find("input", {"id": "gmrq"})["value"])
        data['repairtime'] = str(bsObj.find("input", {"id": "yyazsj"})["value"])  # 上门时间/预约安装时间
        data['orderstatus'] = bsObj.find("span", {"id": "dqpgjd"}).text.strip()
        data['province'] = self.get_selected(bsObj.find("select", {"id": "sfen"}))
        data['city'] = self.get_selected(bsObj.find("select", {"id": "cshi"}))
        data['county'] = self.get_selected(bsObj.find("select", {"id": "xian"}))
        data['town'] = self.get_selected(bsObj.find("select", {"id": "jied"}))
        data['address'] = str(bsObj.find("input", {"id": "dizi"})["value"])
        data['originname'] = self.get_selected(bsObj.find("select", {"id": "xslx"}))  # 销售类型 作为工单来源
        return data

    def logout(self):
        url = self.baseurl + "logout.jsp"
        self.headers['Referer'] = self.baseurl + 'loginAction_login'
        self.session.get(url, headers=self.headers)


if __name__ == '__main__':
    util = GreeUtil('S91898010070', 'S91898010070', adminid='24', factoryid='1')
    print("loadMain result = {}".format(util.loadMain()))
    util.logout()
