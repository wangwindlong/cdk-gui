import json
from urllib.parse import urlparse

import requests


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

    def loadMain(self):
        loginurl = self.baseurl + "/services/organization/api/authenticate"
        data = {"username": self.username, "password": self.passwd, "rememberMe": True}
        self.headers['Referer'] = self.baseurl
        response = self.session.post(loginurl, headers=self.headers, data=json.dumps(data))
        response.encoding = 'utf-8'
        author = response.headers['Authorization']
        self.headers['Authorization'] = author
        # print("loadMain author={}".format(author))
        return self.getUserInfo()

    def getUserInfo(self):
        loginurl = self.baseurl + "/services/organization/api/current/dept/info"
        self.headers['Referer'] = self.baseurl
        response = self.session.get(loginurl, headers=self.headers)
        response.encoding = 'utf-8'
        return self.login()

    def login(self):
        loginurl = self.baseurl + "/services/organization/api/ourmUser/login"
        self.headers['Referer'] = self.baseurl
        response = self.session.get(loginurl, headers=self.headers)
        response.encoding = 'utf-8'
        return self.getOrgInfo()

    def getOrgInfo(self):
        loginurl = self.baseurl + "/services/organization/api/ourmUser/list"
        self.headers['Referer'] = self.baseurl
        response = self.session.get(loginurl, headers=self.headers)
        response.encoding = 'utf-8'
        params = [
            # {"betweenMap": {}, "dto": {"status": "DISTRIBUTING"}, "extMap": {}, "searchMap": {}},
            {"dto": {"status": "ACCEPTED"}, "pageIndex": 1, "pageSize": 50},
            {"dto": {"status": "RESERVATION"}, "betweenMap": {}, "searchMap": {}, "pageIndex": 1, "pageSize": 50}]
        orderlist = []
        for param in params:
            orders = self.loadOrders(param)
            if orders and len(orders) > 0:
                orderlist += orders
        print("orderlist count={} orderlist={}".format(len(orderlist), orderlist))
        try:
            data = {"data": json.dumps(orderlist)}
            requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
        except Exception as e:
            print("addorder failed:", e)
            return self.datafail
        return self.datasuccess

    def loadOrders(self, param=None):
        orderurl = self.baseurl + "/services/distributeproce/api/repair/acl/_search/page"
        # RESERVATION 待确认 ACCEPTED 待预约 DISTRIBUTING 待接单  VISIT 待完工
        # 维修任务
        # {"betweenMap":{},"dto":{"type":"REPAIR_ACL_OWN_NOT"},"searchMap":{"status":{"opt":"IN","value":"SUBMIT,ACCEPTED,RESERVATION,VISIT"}},"pageIndex": 1,"pageSize":10}
        # params = {"betweenMap": {}, "dto": {"status": "DISTRIBUTING"}, "extMap": {}, "searchMap": {}, "pageIndex": 1, "pageSize": 50}
        # params = {"dto": {"status": "ACCEPTED"}, "pageIndex": 1, "pageSize": 50}
        self.headers['Request-Source'] = 'PC'
        self.headers['Sec-Fetch-Dest'] = 'empty'
        response = self.session.post(orderurl, data=json.dumps(param), headers=self.headers)
        response.encoding = 'utf-8'
        datas = json.loads(response.text)
        # print("====================================loadOrders")
        # print(params)
        # print(response.text)
        if datas['status'] == 200:
            try:
                return self.parseOrders(datas)
            except Exception as e:
                print("addorder failed:", e)
        return []

    def parseOrders(self, datas):
        total_num = datas['data']['totalElements']
        order_list = []
        for order_key in datas['data']['content']:
            # repairSubOrderNum ："PD2020042801002-01"  repairNum ："PD2020042801002" reportNum ：BDX2020042800717
            repairtime = order_key['reservationDate'] if not order_key['reservationFirstTime'] else order_key[
                'reservationFirstTime'] if not order_key['reservationSuccessTime'] else order_key[
                'reservationSuccessTime']
            if repairtime:
                repairtime = repairtime.replace("T", ' ')
            orderno = order_key['repairSubOrderNum'] if order_key['repairSubOrderNum'] else order_key['reportNum']
            order_info = {'factorynumber': orderno, 'ordername': order_key['serviceTypeName'],
                          'username': order_key['purchaserName'], 'mobile': order_key['purchaserPhone'],
                          'orderstatus': order_key['statusName'], 'originname': '康佳系统',
                          'mastername': order_key['repairAclName'],
                          'machinetype': order_key['seriesName'], 'machinebrand': '康佳', 'sn': '',
                          'companyid': self.factoryid, 'adminid': self.adminid,
                          'address': str(order_key['purchaserReportAddress']),
                          'province': order_key['provinceName'], 'city': order_key['cityName'],
                          'county': order_key['regionName'], 'town': order_key['countyName'],
                          'ordertime': order_key['createdDate'], 'repairtime': repairtime,
                          'note': str(order_key['brandName']) + str(order_key['serviceNatureName']),
                          'description': order_key['userFaultDesc'],
                          }
            order_list.append(order_info)
        return order_list


if __name__ == '__main__':
    # util = ConkaUtil('K608475', 'Kuser6646!', adminid='20699', factoryid='1')
    util = ConkaUtil('K608475', 'Kuser6646!', adminid='24', factoryid='1')
    # util = ConkaUtil('K608069', 'Crm@20200401', adminid='24', factoryid='1')
    print(util.loadMain())
