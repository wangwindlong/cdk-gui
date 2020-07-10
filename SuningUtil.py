import json
import time
from datetime import date, timedelta
from urllib import parse

import requests

from BaseUtil import BaseUtil
from cookie_test import fetch_chrome_cookie


class SuningUtil(BaseUtil):

    def __init__(self, username, passwd, adminid='24', factoryid='4', baseurl='http://ases.suning.com',
                 bjdomain='http://yxgtest.bangjia.me'):
        super(SuningUtil, self).__init__(username, passwd, adminid, factoryid, baseurl, bjdomain)
        self.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng," \
                                 "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        # self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        self.headers['Upgrade-Insecure-Requests'] = '1'
        self.headers['Accept-Encoding'] = 'gzip, deflate'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
        self.cookie = fetch_chrome_cookie([
            {"domain": "ases.suning.com"},
            {"domain": ".ases.suning.com"},
            {"domain": ".suning.com"},
            {"domain": "tianyan.suning.com"},
        ], isExact=True)
        self.cookies = BaseUtil.getCookies(self.cookie)
        self.headers['Cookie'] = self.cookie
        # print(self.cookie)
        self.userinfo = None

    def loadBI(self, param=None):
        # print("===================loadBI")
        loginurl = "http://ases.suning.com/ases-web/main/homeServiceOrders/biSmgzbb.action"
        header = self.headers.copy()
        header[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        del header['Content-Type']
        del header['Origin']
        header['Host'] = 'ases.suning.com'
        header['Referer'] = 'http://ases.suning.com/ases-web/index.html'
        loginRes = self.session.get(loginurl, headers=self.headers)
        # print(loginRes.headers)
        # print(loginRes.text)

    def loadMenu(self, param=None):
        # print("===================loadMenu")
        loginurl = self.baseurl + "/ases-web/main/menu/queryMenu.action?pId=FUN_18_02"
        self.headers['Accept'] = 'application/json, text/plain, */*'
        self.headers['Referer'] = self.baseurl+'/ases-web/index.html'
        menuRes = self.session.get(loginurl, headers=self.headers)
        # print(menuRes.headers)  # FUN_18_02_33 BI   FUN_18_02_04:改派工人管理
        # print(menuRes.text)

    def getUserinfo(self, param=None):
        # self.loadMenu()
        # print("===================getUserinfo")
        loginurl = self.baseurl + "/ases-web/main/user/userInfo.action"
        self.headers['Accept'] = 'application/json, text/plain, */*'
        self.headers['Referer'] = self.baseurl + '/ases-web/index.html'
        userinfo = self.getjson(self.session.get(loginurl, headers=self.headers))
        # print(userinfo)
        if userinfo and userinfo['result'] and userinfo['data']:
            wd = userinfo['data']['wd']
            supplierCode = userinfo['data']['supplierCode']
            userId = userinfo['data']['userId']
            companyCode = userinfo['data']['companyCode'][0]
            result = {"wd": wd, "supplierCode": supplierCode, "userId": userId, "companyCode": companyCode}
            return result
        return None

    def loadOrders(self, param=None):
        if not self.userinfo:
            self.userinfo = self.getUserinfo()
        if not self.userinfo:
            return self.datafail
        # print("=================================loadOrders")
        # 开始加载工单
        self.headers['Accept'] = "application/json, text/plain, */*"
        self.headers['Content-Type'] = 'application/json'
        url = self.baseurl + "/ases-web/main/ui/dispatchWorker/queryList.action"
        params = {"wds": self.userinfo['wd'], "companyCode": self.userinfo['companyCode'],
                  "srvTimeStart": (date.today() - timedelta(days=3)).strftime("%Y-%m-%d"),
                  "srvTimeEnd": (date.today() + timedelta(days=3)).strftime("%Y-%m-%d"),
                  "page": "1", "pageSize": "100"
                  }
        url = url + "?" + str(parse.urlencode(params))
        orderRes = self.session.get(url, headers=self.headers)
        # self.loadBI()
        try:
            data = {"data": json.dumps(self.parseOrders(orderRes))}
            # print(data)
            requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
        except:
            return self.dataverify
        return self.datasuccess

    def parseOrders(self, orderRes):
        datas = self.getjson(orderRes)
        orders = []
        if datas and 'result' in datas and datas['result'] and datas['data']:
            items = datas['data']['datas']
        else:
            return orders
        for item in items:
            orders.append({
                'factorynumber': item['orderId'], 'ordername': item['operateItemDec'],
                'username': item['consignee'], 'mobile': item['mobPhoneNum'],
                'orderstatus': "改派工人", 'originname': "苏宁",
                # 'machinetype': item['PROD_NAME'], 'machinebrand': item['BRAND_NAME'],
                'sn': item['cmmdtyCode'], 'version': item['cmmdtyName'] if 'cmmdtyName' in item else '',
                'repairtime': item['srvTime'] if 'srvTime' in item else '',
                'mastername': item['zyry1BpName'] if 'zyry1BpName' in item else '',
                'note': item['srvMemo'] if 'srvMemo' in item else '',
                'companyid': self.factoryid, 'adminid': self.adminid,
                'address': str(item['srvAddress']).replace(";", "").strip(),
                # 'province': item['provinceName'], 'city': item['cityName'],
                # 'county': item['regionName'], 'town': item['countyName'],
                'description': str(item['orderType']) + self.parseOrderType(item['orderType']),
            })
        return orders

    def parseOrderType(self, ordertype):
        if ordertype == "ZS01":
            return "新机安装"
        elif ordertype == "ZS02":
            return "辅助安装"
        elif ordertype == "ZS03":
            return "移机"
        elif ordertype == "ZS04":
            return "退换货拆装"
        elif ordertype == "ZS06":
            return "上门维修"
        elif ordertype == "ZS09":
            return "用户送修检测"
        elif ordertype == "ZS10":
            return "用户送修维修"
        elif ordertype == "ZS11":
            return "上门鉴定"
        elif ordertype == "ZS12":
            return "清洗/保养"
        elif ordertype == "ZS24":
            return "家电回收"
        elif ordertype == "ZS30":
            return "家装"
        else:
            return "安装"


if __name__ == '__main__':
    util = SuningUtil('W850018433', 'sn789456', adminid='24', factoryid='99')
    print(util.loadOrders())
