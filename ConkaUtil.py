import datetime
import json
import re
import time
from urllib import parse
from urllib.parse import urlparse

import requests
from cookie_test import fetch_chrome_cookie


class ConkaUtil:
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
        # self.session = HTMLSession()
        # self.agent = random.choice(agents)
        self.agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/81.0.4044.113 Safari/537.36'
        self.datasuccess = {'code': 1, 'msg': '抓单成功', 'element': ''}
        self.datafail = {'code': 0, 'msg': '抓单失败,请确认账号密码是否正确'}
        self.headers = {'content-type': 'application/json;charset=utf-8',
                        'User-Agent': self.agent,
                        'Upgrade-Insecure-Requests': '1', 'Host': self.host, 'Origin': self.baseurl,
                        'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Accept': 'application/json, text/plain, */*'}

    def loadMain(self):
        loginurl = self.baseurl + "/services/organization/api/authenticate"
        data = {"username": self.username, "password": self.passwd, "rememberMe": True}
        self.headers['Referer'] = self.baseurl
        response = self.session.post(loginurl, headers=self.headers, data=json.dumps(data))
        response.encoding = 'utf-8'
        # orgIds = re.findall(r"var orgId = \"(.+?)\"", response.text, re.S)
        datas = json.loads(response.text)
        print(response.text)
        print("================================getUserInfo")
        author = response.headers['Authorization']
        print(author)
        self.headers['Authorization'] = author
        self.getUserInfo()
        # if datas['code'] != 1 or not datas['result']:
        #     return self.datafail
        # orgIds = datas['result']
        # if not orgIds or len(orgIds) <= 0:
        #     return self.datafail
        # # originOrgId = re.findall(r"originOrgId: '(.+?)',", response.text, re.S)[0]
        # # orgId = orgIds[0]
        # orgId = orgIds[0]['id']
        # originOrgId = orgId
        # # print(originOrgId)
        # return self.loadOrders({'orgId': orgId, "originOrgId": originOrgId})

    def getUserInfo(self):
        loginurl = self.baseurl + "/services/organization/api/current/dept/info"
        self.headers['Referer'] = self.baseurl
        response = self.session.get(loginurl, headers=self.headers)
        response.encoding = 'utf-8'
        # orgIds = re.findall(r"var orgId = \"(.+?)\"", response.text, re.S)
        # datas = json.loads(response.text)
        print(response.text)
        print("================================login")
        self.login()

    def login(self):
        loginurl = self.baseurl + "/services/organization/api/ourmUser/login"
        self.headers['Referer'] = self.baseurl
        response = self.session.get(loginurl, headers=self.headers)
        response.encoding = 'utf-8'
        # orgIds = re.findall(r"var orgId = \"(.+?)\"", response.text, re.S)
        # datas = json.loads(response.text)
        print(response.text)
        print("================================getOrgInfo")
        self.getOrgInfo()

    def getOrgInfo(self):
        loginurl = self.baseurl + "/services/organization/api/ourmUser/list"
        self.headers['Referer'] = self.baseurl
        response = self.session.get(loginurl, headers=self.headers)
        response.encoding = 'utf-8'
        # orgIds = re.findall(r"var orgId = \"(.+?)\"", response.text, re.S)
        # datas = json.loads(response.text)
        print(response.text)
        print("================================loadOrders")
        self.loadOrders()

    def loadOrders(self, param=None):
        orderurl = self.baseurl + "/services/distributeproce/api/repair/acl/_search/page"
        # RESERVATION 待确认 ACCEPTED 待预约 DISTRIBUTING 待接单  VISIT 待完工
        # {"betweenMap":{},"dto":{"status":"DISTRIBUTING"},"extMap":{},"searchMap":{},"pageIndex":1,"pageSize":50}
        # 维修任务
        # {"betweenMap":{},"dto":{"type":"REPAIR_ACL_OWN_NOT"},"searchMap":{"status":{"opt":"IN","value":"SUBMIT,ACCEPTED,RESERVATION,VISIT"}},"pageIndex": 1,"pageSize":10}
        params = {"dto": {"status": "RESERVATION"}, "pageIndex": 1, "pageSize": 50}
        response = self.session.post(orderurl, data=json.dumps(params), headers=self.headers)
        response.encoding = 'utf-8'
        print(response.text)
        datas = json.loads(response.text)
        print(datas['result']['pageInfo']['total'])
        if datas['status'] == 200:
            try:
                data = {"data": json.dumps(self.parseOrders(datas))}
                requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
            except:
                return self.datafail
            return self.datasuccess
        return self.datafail

    def parseOrders(self, datas):
        total_num = datas['result']['pageInfo']['total']
        # print("total count:{}".format(total_num))
        order_list = []
        for order_key in datas['result']['srvInfos']:
            # flag = 0
            # for key in order_list:
            #     if (order_list[key]['factorynumber'] == order_key['sId']):
            #         order_list[key]['sn'] = order_list[key]['sn'] + "," + order_key['sns']
            #         flag = 1
            #         break
            # if flag == 1:
            #     continue
            order_info = {'factorynumber': order_key['sId'], 'ordername': order_key['typeDesc'],
                          'username': order_key['customerName'], 'mobile': order_key['customerTel'],
                          'orderstatus': order_key['statusDesc'],
                          'machinetype': order_key['goodsNames'].replace("小米", ''), 'sn': order_key['sns'],
                          'companyid': self.factoryid, 'machinebrand': '小米', 'originname': '小米系统',
                          'adminid': self.adminid}
            order_list.append(self.getDetail(order_info, order_key))
        return order_list

    # 查询详情接口
    def getDetail(self, order, datas):
        self.headers['Referer'] = self.mainurl
        post_data = "method=srvServicing.getCommonSrvDetail&params=%7B%22sId%22%3A%22" + datas['sId'] + \
                    "%22%2C%22conditions%22%3A%22BASEINFO%22%7D"
        response = self.session.post(self.searchurl, data=post_data, headers=self.headers)
        response.encoding = 'utf-8'
        json_ret2 = json.loads(response.text)
        if json_ret2['code'] == 1:
            order['address'] = json_ret2['result']['baseInformation']['addressDesc']
            timeArray = time.localtime(json_ret2['result']['baseInformation']['applyTime'] / 1000)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            order['ordertime'] = otherStyleTime
            if json_ret2['result']['baseInformation']['hopeVisitTime']:
                order['repairtime'] = json_ret2['result']['baseInformation']['hopeVisitTime']
        createFrom = json_ret2['result']['baseInformation']['createFrom']
        if createFrom.find("预付费") != -1 and createFrom != '':
            order['note'] = createFrom
            if len(json_ret2['result']['baseInformation']['items']) > 0:
                priceitem = json.loads(json_ret2['result']['baseInformation']['items'][0]['extendContent'])
                order['note'] = order['note'] + str(priceitem['price'])
        return self.getDescription(order, datas)

    # 查询处理结果，问题描述
    def getDescription(self, order, datas):
        self.headers['Referer'] = self.searchurl + '?router=service_info_detail&sId=' + datas['sId']
        post_data = "method=srvServicing.getServiceVo&params=%7B%22sId%22%3A%22" + datas[
            'sId'] + "%22%2C%22conditions%22%3A%22%22%7D"
        response = self.session.post(self.searchurl, data=post_data, headers=self.headers)
        response.encoding = 'utf-8'
        json_ret3 = json.loads(response.text)
        if json_ret3['code'] == 1:
            data = json_ret3['result']
            if data['customerDesc']:
                order['description'] = data['customerDesc']
            fault = ''
            if len(data['items']) > 0:
                for item in data['items'][0]['itemHasFaults']:
                    fault += item['faultName'] + ";"
                if data['items'][0]['faultDesc']:
                    fault += data['items'][0]['faultDesc'] + ";"
                if data['items'][0]['methods']:
                    fault += "处理方法:" + data['items'][0]['methods'][0]['name']
            if fault:
                order['note'] = fault
        return order


if __name__ == '__main__':
    util = ConkaUtil('K608475', 'Kuser6646!', factoryid='1')
    # util = ConkaUtil('K608069', 'Crm@20200401', factoryid='17')
    print(util.loadMain())
