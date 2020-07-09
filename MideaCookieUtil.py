import json
import time
from datetime import date, timedelta

import requests

from BaseUtil import BaseUtil
from cookie_test import fetch_chrome_cookie


class MideaUtil(BaseUtil):

    def __init__(self, username, passwd, adminid='24', factoryid='4', baseurl='https://cs.midea.com/c-css/',
                 bjdomain='http://yxgtest.bangjia.me'):
        super(MideaUtil, self).__init__(username, passwd, adminid, factoryid, baseurl, bjdomain)
        self.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng," \
                                 "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

        self.headers['Accept'] = "*/*"
        self.headers['Content-Type'] = 'application/json'
        self.cookie = fetch_chrome_cookie([{"domain": ".midea.com"}], isExact=False)
        self.cookies = BaseUtil.getCookies(self.cookie)
        self.headers['Cookie'] = self.cookie
        print("init cookie=", self.cookie)

    def loadOrders(self, param=None):
        # 开始加载工单
        try:
            data = {"data": json.dumps(self.loadRolesOrder())}
            print("loadOrders data=", data)
            requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
        except:
            return self.dataverify
        return self.datasuccess

    def loadRolesOrder(self):
        roleurl = self.baseurl + "desktop/userInfo"
        self.headers['Referer'] = self.baseurl + "views/css/desktop/index.jsp"
        response = self.session.post(roleurl, headers=self.headers)
        print("userInfo result=", response.text)
        result = []
        if response.status_code == 200 and response.text:
            roleresult = self.getjson(response)
            if not roleresult or 'status' not in roleresult or not roleresult['status']:
                return self.datafail
            if 'content' not in roleresult or 'orgUsers' not in roleresult['content']:
                return self.datafail
            for org in roleresult['content']['orgUsers']:
                orgId = org['orgEntityVO']['orgCode']
                result = self.merge(result, self.switchOrg(orgId), "factorynumber")

    def switchOrg(self, orgId):
        roleurl = self.baseurl + "switchOrg"
        self.headers['Referer'] = self.baseurl + "views/css/desktop/index.jsp"
        params = {"currentOrg": orgId, "loginToken": self.cookies['loginToken']}
        response = self.session.post(roleurl, headers=self.headers, data=params)
        # self.initCookie()
        # print("switchOrg orgId={}，params={}, result={} ".format(orgId, params, response.text))
        response = self.session.get(self.baseurl + 'views/css/desktopPlugIn/wd_homePage.jsp', headers=self.headers)
        # print("wd_homePage orgId={}，params={}, result={} ".format(orgId, params, response.text))
        return list(self.loadPageOrder())

    def loadPageOrder(self, page=1, totalcount=100, pageSize=100):
        dataurl = self.baseurl + "wom/serviceorderunit/listdata"
        data = {"page": page, "rows": pageSize, "pageIndex": page - 1, "pageSize": pageSize,
                "formConditions": {"SERVICE_ORDER_STATUS": "", "CONTAIN_EJFWS": "N",
                                   "CONTACT_TIME": (date.today() - timedelta(days=3)).strftime("%Y-%m-%d"),
                                   "CONTACT_TIME_end": (date.today()).strftime("%Y-%m-%d")}}
        response = self.session.post(dataurl, headers=self.headers, data=json.dumps(data))
        self.headers['Referer'] = self.baseurl + "wom/serviceorderunit/list?type=womServiceNotFinshCount"
        response.encoding = 'utf-8'
        print("loadOrders response={}".format(response.text))
        result = json.loads(response.text)
        if result and 'status' in result and result['status']:
            data = result['content']
            totalcount = data['total']
            pagecount = data['pageCount']
            pageSize = data['pageSize']
            page = data['pageIndex']
            # print("totalcount={} pagecount={} pageSize={} page={}".format(totalcount, pagecount, pageSize, page))
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
    # bangjia:13819807915 美的：AW3306009461 Md123456789
    util = MideaUtil('AW3306009461', 'Md123456789!', adminid='24', factoryid='4')
    # util = ConkaUtil('K608069', 'Crm@20200401', adminid='24', factoryid='1')
    print(util.loadOrders())
