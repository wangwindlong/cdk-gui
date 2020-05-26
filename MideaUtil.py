import json
import time
from datetime import date, timedelta

import requests

from BaseUtil import BaseUtil


class MideaUtil(BaseUtil):

    def __init__(self, username, passwd, adminid='24', factoryid='4', baseurl='https://cs.midea.com/c-css/',
                 bjdomain='http://yxgtest.bangjia.me'):
        super(MideaUtil, self).__init__(username, passwd, adminid, factoryid, baseurl, bjdomain)
        self.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng," \
                                 "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        self.dataverify = {'code': 2, 'msg': '输入验证码', 'element': ''}

    def login(self, param=None):
        self.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng," \
                                 "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        if not param:
            loginurl = self.baseurl + "login"
            self.headers['Referer'] = loginurl
            response = self.session.get(loginurl, headers=self.headers)
            response.encoding = 'utf-8'
            print("login statuscode={}".format(response.status_code == 200))
            print("login response={}".format(response.text))
            if response.status_code == 200:
                result = self.loginauth()
            else:
                return self.getCaptcha()
        else:
            result = self.loginauth(param)
        print("login result={}".format(result))
        print("param={}".format(param))
        return param

    def getCaptcha(self):
        self.dataverify['url'] = self.baseurl + "captcha?r={}".format(round(time.time()*1000))
        return self.dataverify

    def loginauth(self, param=None):
        code = param['code'] if param and 'code' in param else param
        if not code:
            if not self.checkState():
                return self.getCaptcha()
            else:
                code = ''
        authurl = self.baseurl + "signin"
        data = {"userAccount": self.username,
                "userPassword": "6d904a32d4dbf2db15336eadca0d4802edfe2f85c0da02a32bff93b70c8d0b2c7181fd58c434c7838dd2b234feda762fbca546967a5ea7568958f55bc7966dd1",
                "captcha": code, "domainType": "CS"}
        print("loginauth data={}".format(data))
        response = self.session.post(authurl, headers=self.headers, data=data)
        self.headers['Referer'] = authurl
        response.encoding = 'utf-8'
        print("loginauth result={}".format(response.text))
        if response.status_code == 200:
            result = json.loads(response.text)
            if result and 'status' in result and result['status']:
                return self.loadOrders(True)
        return self.datafail

    def checkState(self):
        checkurl = self.baseurl + "captchaState"
        data = {"userAccount": self.username}
        response = self.session.post(checkurl, headers=self.headers, data=data)
        response.encoding = 'utf-8'
        result = False
        print("checkstate response={}".format(response.text))
        if response.status_code == 200:
            state = json.loads(response.text)
            if state and 'content' in state and not state['content']:
                result = True
            else:
                result = False
        print("checkstate result={}".format(result))
        return result

    def isLogin(self):
        self.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng," \
                                 "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        mainurl = self.baseurl + "views/css/desktop/index.jsp"
        print(mainurl)
        response = self.session.get(mainurl, headers=self.headers)
        response.encoding = 'utf-8'
        print("loadOrders response={}".format(response.text))
        if response.status_code == 200 and not response.text.startswith("<script>"):
            return True
        return False

    def loadOrders(self, param=None):
        if not param and not self.isLogin():
            return self.login()
        try:
            data = {"data": json.dumps(list(self.loadPageOrder()))}
            requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
        except:
            return self.datafail
        return self.datasuccess

    def loadPageOrder(self, page=1, totalcount=100, pageSize=100):
        # 开始加载工单
        self.headers['Accept'] = "*/*"
        self.headers['Content-Type'] = 'application/json'
        dataurl = self.baseurl + "womflow/serviceorderunit/listdata"
        data = {"page": page, "rows": pageSize, "pageIndex": page - 1, "pageSize": pageSize,
                "formConditions": {"SERVICE_ORDER_STATUS": "",
                                   "CONTACT_TIME": (date.today() - timedelta(days=7)).strftime("%Y-%m-%d"),
                                   "CONTACT_TIME_end": (date.today()).strftime("%Y-%m-%d")}}
        response = self.session.post(dataurl, headers=self.headers, data=json.dumps(data))
        self.headers['Referer'] = self.baseurl + "womflow/serviceorderunit/list?type=womServiceNotFinshCount"
        response.encoding = 'utf-8'
        print("loadOrders response={}".format(response.text))
        result = json.loads(response.text)
        if result and 'status' in result and result['status']:
            data = result['content']
            totalcount = data['total']
            pagecount = data['pageCount']
            pageSize = data['pageSize']
            page = data['pageIndex']
            print("totalcount={} pagecount={} pageSize={} page={}".format(totalcount, pagecount, pageSize, page))
            if page >= pagecount:
                yield from self.parseOrders(data)
            else:
                yield from self.parseOrders(data)
                yield from self.loadPageOrder(page + 1, totalcount, pageSize)

    def parseOrders(self, data):
        for item in data['rows']:
            yield {
                'factorynumber': item['SERVICE_ORDER_NO'], 'ordername': item['SERVICE_SUB_TYPE_NAME'],
                'username': item['SERVICE_CUSTOMER_NAME'], 'mobile': item['SERVICE_CUSTOMER_TEL1'],
                'orderstatus': item['SERVICE_ORDER_STATUS'], 'originname': item['ORDER_ORIGIN'],
                'machinetype': item['PROD_NAME'], 'machinebrand': item['BRAND_NAME'],
                'sn': '', 'version': item['PRODUCT_MODEL'] if 'PRODUCT_MODEL' in item else '',
                'repairtime': item['FINAL_APPOINT_TIME'] if 'FINAL_APPOINT_TIME' in item else '',
                'mastername': item['ENGINEER_NAME'] if 'ENGINEER_NAME' in item else '',
                'note': item['PUB_REMARK'] if 'PUB_REMARK' in item else '',
                'companyid': self.factoryid, 'adminid': self.adminid,
                'address': str(item['SERVICE_CUSTOMER_ADDRESS']),
                # 'province': item['provinceName'], 'city': item['cityName'],
                # 'county': item['regionName'], 'town': item['countyName'],
                'ordertime': item['CONTACT_TIME'],
                'description': item['SERVICE_DESC'],
            }


if __name__ == '__main__':
    # util = ConkaUtil('K608475', 'Kuser6646!', adminid='20699', factoryid='1')
    util = MideaUtil('AW3306009461', 'Md123456789!', adminid='24', factoryid='4')
    # util = MideaUtil('Aw3302060387', 'Jj62721262', adminid='24', factoryid='4')
    # util = ConkaUtil('K608069', 'Crm@20200401', adminid='24', factoryid='1')
    print(util.loadOrders())
