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
        self.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        self.cookie = fetch_chrome_cookie([
            {"domain": "ases.suning.com"},
            {"domain": ".ases.suning.com"},
            {"domain": ".suning.com"},
            {"domain": "tianyan.suning.com"},
        ], isExact=True)
        self.cookie = "JSESSIONID=qlx9uFTy9LJC5Z1lYZlerT3z.asesprdapp68; userIdKey=88fdaf7e74e04d349b67b49ce3a6eea3; loginUserId=W850018433; route=7d8521d7a68070d623043983a9b3dac2; iar_sncd=0; _df_ud=9fe5d898-d6d4-4e40-b7b4-b4c2b3ceb1d0; rememberUserNameKey=W850018433; _snvd=1594020788106mrkUUmAE1la; tradeMA=155; authId=siF7A9632AC69AB42447BB7FA9E2832184; streetCode=0210199; SN_CITY=20_021_1000267_9264_01_12113_2_0; cityCode=021; districtId=12113; cityId=9264; token=2687c752-5d3d-4930-9d3d-27efd4339499; hm_guid=6812c016-6b48-4b32-84e4-d1dc07d92785; _device_session_id=p_939e0ec2-911e-49d4-b72e-009a49e937f1; _snzwt=THMfYO1732fdab8c5Y0AU61eb; _snsr=direct%7Cdirect%7C%7C%7C; CSRF-TOKEN=5occ9cotaydj1co5535qcrvvlkr9w545arpj; _snmc=1; _snma=1%7C159402078808640074%7C1594020788086%7C1594238607707%7C1594245064400%7C16%7C3; _snmp=159424506432878292; _snmb=159424506441715057%7C1594245064497%7C1594245064417%7C1"
        self.cookies = BaseUtil.getCookies(self.cookie)
        self.headers['Cookie'] = self.cookie
        # print(self.cookie)
        self.userinfo = None

    def loadBI(self, param=None):
        print("===================loadBI")
        loginurl = "http://ases.suning.com/ases-web/main/homeServiceOrders/biSmgzbb.action"
        header = self.headers.copy()
        header[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        del header['Content-Type']
        del header['Origin']
        header['Host'] = 'ases.suning.com'
        header['Referer'] = 'http://ases.suning.com/ases-web/index.html'
        loginRes = self.session.get(loginurl, headers=self.headers)
        print(loginRes.headers)
        print(loginRes.text)

    def loadMenu(self, param=None):
        # print("===================loadMenu")
        loginurl = "http://ases.suning.com/ases-web/main/menu/queryMenu.action?pId=FUN_18_02"
        self.headers['Accept'] = 'application/json, text/plain, */*'
        del self.headers['Content-Type']
        self.headers['Origin'] = 'http://ases.suning.com'
        self.headers['Host'] = 'ases.suning.com'
        self.headers['Referer'] = 'http://ases.suning.com/ases-web/index.html'
        menuRes = self.session.get(loginurl, headers=self.headers)
        # print(menuRes.headers)  # FUN_18_02_33 BI   FUN_18_02_04:改派工人管理
        # print(menuRes.text)
        if menuRes and menuRes['result'] and menuRes['data']:
            context = menuRes['data']['contextPath']
            funList = menuRes['data']['funList']
            # for fun in funList:
            # if fun['functionCode'] == 'FUN_18_02_04' or fun['functionCode'] == 'FUN_18_02_33':

    def getUserinfo(self, param=None):
        # print("===================getUserinfo")
        loginurl = self.baseurl + "/ases-web/main/user/userInfo.action"
        self.headers['Accept'] = 'application/json, text/plain, */*'
        del self.headers['Content-Type']
        self.headers['Origin'] = 'http://ases.suning.com'
        self.headers['Host'] = 'ases.suning.com'
        self.headers['Referer'] = 'http://ases.suning.com/ases-web/index.html'
        userinfo = self.getjson(self.session.get(loginurl, headers=self.headers))
        # print(loginRes.headers)
        # print(loginRes.text)
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
                  "srvTimeStart": (date.today() - timedelta(days=5)).strftime("%Y-%m-%d"),
                  "srvTimeEnd": date.today().strftime("%Y-%m-%d"),
                  "page": "1", "pageSize": "100"
                  }
        url = url + "?" + str(parse.urlencode(params))
        orderRes = self.session.get(url, headers=self.headers)
        # self.loadBI()
        try:
            data = {"data": json.dumps(self.parseOrders(orderRes))}
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
    util = SuningUtil('W850018433', 'sn789456*', adminid='24', factoryid='99')
    print(util.loadOrders())
