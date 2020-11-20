import datetime
import json
import re
import time
from urllib import parse
from urllib.parse import urlparse

import requests
from BaseUtil import BaseUtil
from cookie_test import fetch_chrome_cookie


class CDKCookieUtil(BaseUtil):

    def __init__(self, username='', passwd='', adminid='24', factoryid='18', baseurl='http://cdk.rrs.com',
                 bjdomain='http://yxgtest.bangjia.me'):
        super(CDKCookieUtil, self).__init__(username, passwd, adminid, factoryid, baseurl, bjdomain)
        self.headers['Accept'] = "application/json, text/plain, */*"
        self.headers['Content-Type'] = 'application/json'
        self.cookie = fetch_chrome_cookie([{"domain": ".rrs.com"}], isExact=False)
        self.cookies = BaseUtil.getCookies(self.cookie)
        self.headers['Cookie'] = self.cookie
        self.azbaseurl = ''  # cdk安装的baseurl，海尔安装单要用到：http://cdkaz.rrs.com
        self.azhost = ''  # cdk安装的host：cdkaz.rrs.com

    def loadOrders(self, param=None):
        # # 开始加载工单
        # self.headers['Accept'] = "*/*"
        # self.headers['Content-Type'] = 'application/json'
        # try:
        #     data = {"data": json.dumps(list(self.loadPageOrder()))}
        #     requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
        # except:
        #     return self.dataverify
        # return self.datasuccess
        # print(self.cookies)
        if not self.islogin():
            return self.dataverify
        isSuccess = True
        haierRes = self.loadHaierOrder()  # 抓取海尔工单
        # print("loadHaierOrder result=", haierRes)
        isSuccess = isSuccess and haierRes['code'] == 1
        netorder = self.loadWangdan()
        # 1: 表示维修 2 表示安装 3 表示鸿合维修单 4 表示清洁保养"""
        if not netorder:
            return self.dataverify
        netRes = self.loadNetworkOrder(netorder, 5)  # 抓取网单 - 所有
        isSuccess = isSuccess and netRes['code'] == 1
        # netRes = self.loadNetworkOrder(netorder, 2)  # 抓取网单 - 安装
        # isSuccess = isSuccess and netRes['code'] == 1
        # netRes = self.loadNetworkOrder(netorder, 1)  # 抓取网单 - 维修
        # isSuccess = isSuccess and netRes['code'] == 1
        # netRes = self.loadNetworkOrder(netorder, 3)  # 抓取网单 - 鸿合维修单
        # isSuccess = isSuccess and netRes['code'] == 1
        # netRes = self.loadNetworkOrder(netorder, 4)  # 抓取网单 - 清洁保养
        # isSuccess = isSuccess and netRes['code'] == 1
        return self.datasuccess if isSuccess else self.datafail

    def islogin(self):
        url = self.baseurl + "/manager-web/index.do"
        if 'userCookie' in self.cookies:
            url += "?token=" + self.cookies['userCookie']
        header = self.headers.copy()
        header[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        # header['Referer'] = self.baseurl
        response = self.session.get(url, headers=header)
        soup = self.getsoup(response)
        # print(soup)
        haierSpan = soup.find('span', text=re.compile('海尔安装'))
        # print("+++++++++++++++++++++++++++++++getHaierUrl")
        # print(haierSpan)
        if not haierSpan:
            return False
        parsed_url = urlparse(haierSpan['href'])
        self.azhost = parsed_url.netloc
        self.azbaseurl = parsed_url.scheme + "://" + parsed_url.netloc
        params = dict(parse.parse_qsl(parsed_url.query))
        if 'token' not in params:
            return False
        token = params['token']
        self.cookies['token'] = token
        # 进入海尔工单的验证流程
        param = json.dumps({"token": params['token'], "moduleCode": "04", "userId": ""})
        header = self.headers.copy()
        header['Host'] = self.azhost
        header['Origin'] = self.azbaseurl
        header['Referer'] = self.azbaseurl + "/pages/indexcdk?moduleCode=04&newTopWindow=true&token=" + token
        r0 = self.session.post(self.azbaseurl + "/api/system/authMenu/auth", data=param, headers=header)
        r = self.session.post(self.azbaseurl + "/api/system/authMenu/authMenuChanges", data=param, headers=header)
        # r2 = self.session.post(self.baseurl + "/manager-web/getCdkscIndexData.do", headers=header)
        return self.isSuccess(r0) and self.isSuccess(r)  # and self.isSuccess(r2)

    def isSuccess(self, r):
        authresult = self.getjson(r)
        if not authresult or 'success' not in authresult or not authresult['success']:
            return False
        # if 'serviceCode' in authresult and authresult['serviceCode']:
        #     self.serviceCode = authresult['serviceCode']
        return True

    def loadWangdan(self):
        """加载网单页面"""
        url = self.baseurl + "/cdkwd/index2?moduleCode=02&token=" + self.cookies['token']
        header = self.headers
        del header['Content-Type']
        header[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        header['Referer'] = self.baseurl + "/manager-web/index.do?token=" + self.cookies['token']
        header['Upgrade-Insecure-Requests'] = "1"
        response = self.session.get(url, headers=header)
        soup = self.getsoup(response)
        # print(soup)
        haierSpan = soup.find('div', text=re.compile('网单全流程'))
        print("+++++++++++++++++++++++++++++++loadWangdan")
        print(haierSpan)
        if not haierSpan:
            return False
        netorder = {'0': url,
                    # '1': self.baseurl + soup.find('div', text=re.compile('维修单'))['href'],
                    # '2': self.baseurl + soup.find('div', text=re.compile('安装单'))['href'],
                    # '3': self.baseurl + soup.find('div', text=re.compile('鸿合维修单'))['href'],
                    # '4': self.baseurl + soup.find('div', text=re.compile('清洁保养'))['href']
                    '5': self.baseurl + soup.find('div', text=re.compile('网单全流程'))['href']
                    }
        # 1: 表示维修 2 表示安装 3 表示鸿合维修单 4 表示清洁保养""" 5 表示全流程
        return netorder

    def loadNetworkOrder(self, netorder, ordertype=2):
        """:ordertype = 5：所有网单  1: 表示维修 2 表示安装 3 表示鸿合维修单 4 表示清洁保养"""
        api_path = netorder[str(ordertype)]
        # print("***********************************loadNetworkOrder，url={}".format(apiPath))
        header = self.headers
        header['Referer'] = netorder['0']
        self.session.get(api_path, headers=header)
        header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        header[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        header['X-Requested-With'] = "XMLHttpRequest"
        header['Accept-Encoding'] = "gzip, deflate"
        header['Referer'] = api_path
        header['Upgrade-Insecure-Requests'] = '1'
        header['Cache-Control'] = 'max-age=0'

        apiPath = '/cdkwd/azdOrder/azdOrderList'
        if ordertype == 1:
            apiPath = '/cdkwd/repairOrder/repairOrderList'
        elif ordertype == 3:
            apiPath = '/cdkwd/wxRepairOrder/repairOrderList'
        elif ordertype == 4:
            apiPath = '/cdkwd/byOrder/byOrderList'
        elif ordertype == 5:
            apiPath = '/cdkwd/deliveryOrder/deliveryOrderList'

        today = datetime.date.today()  # 获得今天的日期
        pageUrl = self.baseurl + apiPath
        pageUrl = pageUrl + "?orderDateBegin=" + (today - datetime.timedelta(days=26)).strftime(
            '%Y-%m-%d') + "&orderDateEnd=" + datetime.date.today().strftime('%Y-%m-%d')
        pageUrl += "&orderCode=&orderId=&consignee=&length=150&consigneeMobile=&deliveryDateBegin=&deliveryDateEnd=&branchCodeYw=&orderStatus=&carDriver=&carPhone=&province=&city=&regionCode=&consigneeAddr=&carNo=&oldOrder=&isYy=&serviceArea=&serviceCodeYw="
        # params = dict(parse.parse_qsl(parsed_url.query))
        # print("pageUrl={}".format(pageUrl))
        params = {}
        params['draw'] = "2" if ordertype == 2 else "1"  # 1为维修 2为安装
        params['order[0][column]'] = "2"
        params['order[0][dir]'] = "desc"
        params['start'] = 0
        params['length'] = 150
        orderRes = self.session.get(pageUrl, headers=header)
        orderRes.encoding = 'utf-8'
        # print("params=",params)
        # print("headers=",header)
        # print("loadNetworkOrder order result={}".format(orderRes.text))
        if orderRes.status_code != 200 or not orderRes.text or len(orderRes.text.strip()) <= 0:
            return self.datafail
        orderResult = self.getjson(orderRes)
        if 'recordsTotal' in orderResult and orderResult['recordsTotal'] > 0:
            try:
                order_list = list(self.load_wd_orders(orderResult))
                print(order_list)
            except Exception as e:
                error = self.datafail.copy()
                error['msg'] = str(e)
                return error
            checkRes = requests.post(self.bjdomain + "/Api/Climborder/addorder", data={"data": json.dumps(order_list)})
            checkRes.encoding = 'utf-8'
            if checkRes and checkRes.status_code == 200:
                print("网单同步成功")
                return self.datasuccess
        return self.datasuccess

    def load_wd_orders(self, orderResult):  # 加载网单列表
        for r in orderResult['data']:
            description = "原单号:{},工单方式:{},司机:{}|{},联系人:{}|{}".format(r['sourceSn'], r['installWayName'] or '',
                                                                     r['carDriver'] or '', r['carPhone'] or '',
                                                                     r['fhContact'] or '', r['fhMobile'] or '')
            curtime = int(time.time())
            r_time = r['reserveTime'] if r['reserveTime'] else r['deliveryDate'] or str(curtime)
            ordername = r['typeCodeName'] if "typeCodeName" in r and r['typeCodeName'] else ""
            order_info = {'factorynumber': r['orderId'], 'ordername': ordername,
                          'username': r['consignee'], 'mobile': r['consigneeMobile'],
                          'orderstatus': r['orderStatusName'], 'machinetype': r['add8'],
                          'province': r['province'], 'city': r['city'], 'county': r['region'],
                          'address': r['consigneeAddr'], 'description': r['add12'],
                          'ordertime': str(datetime.datetime.fromtimestamp(int(r['createdDate']) / 1000)),
                          'repairtime': str(datetime.datetime.fromtimestamp(int(r_time) / 1000)),
                          'buydate': str(datetime.datetime.fromtimestamp(int(r['accountDate']) / 1000)),
                          'machinebrand': '海尔', 'version': r['add5'], 'note': description,
                          'companyid': self.factoryid, 'adminid': self.adminid,
                          'originname': r['sourceCodeName'],
                          'branchCodeYw': r['branchCodeYw'], 'serviceCodeYw': r['serviceCodeYw']
                          }
            order_info = self.clearAddress(order_info)
            if not self.isNew(order_info, self.bjdomain, self.adminid):
                continue
            yield from self.load_wd_info(order_info)

    def load_wd_info(self, info):  # 加载网单详情
        info_url = self.baseurl + "/cdkwd/deliveryOrder/orderInfo?orderId={}&branchCode={}&serviceCode={}".format(
            info['factorynumber'], info['branchCodeYw'], info['serviceCodeYw'])
        res = self.session.get(info_url, headers=self.headers)
        soup = self.getsoup(res)
        # print("load_wd_info result=", soup)
        m = info['mobile']
        c = m.count('*')
        # print("mobile=", m, "* count=", c)
        mobiles = re.findall(re.compile(r'[>]({})[<]'.format(m.replace("*" * c, "[0-9]{" + str(c) + "}"))), res.text)
        if mobiles and len(mobiles) > 0:
            mobile = mobiles[0]
            info['mobile'] = mobile.split('-')[0]
            info['description'] = "收货人手机:" + mobile
        machines = soup.find("tbody").find('tr').find_all('td')
        if machines and len(machines) > 5:
            info['machinebrand'] = machines[0].text.strip()
            info['machinetype'] = machines[1].text.strip()
            info['version'] = machines[5].text.strip().replace(info['machinebrand'], '').replace(info['machinetype'], "")
            info['sn'] = machines[4].text.strip()
        yield info

    def loadHaierOrder(self):
        pageUrl = self.azbaseurl + '/api/businessData/serviceList/selectServiceDealList'
        # print("***********************************loadHaierOrder,pageUrl=" + pageUrl)
        params = {}
        today = datetime.date.today()  # 获得今天的日期
        params['jobStatus'] = '1#3'  # 只需要一种未派人状态 空则为全部， 1#3#4#5
        params['regTimeStart'] = (today - datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
        params['regTimeEnd'] = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        params['pageIndex'] = 1
        params['rows'] = 50
        params['token'] = self.cookies['token']
        header = self.headers.copy()
        header['Referer'] = 'http://cdkaz.rrs.com/pages/cdkinstall/serveprocess'
        params = json.dumps(params)
        header['Content-Length'] = str(len(params))
        header['Host'] = self.azhost
        header['Origin'] = self.azbaseurl
        # print("loadHaierOrder params:")
        # print("params=", params)
        # print("header=", header)
        # print("pageUrl=", pageUrl)
        orderRes = self.session.post(pageUrl, data=params, headers=header)
        # print(orderRes.text)
        orderResult = self.getjson(orderRes)
        if orderRes.status_code == 200 and 'success' in orderResult and orderResult['success'] and orderResult['data'] \
                and 'records' in orderResult['data'] and orderResult['data']['records']:
            data = orderResult['data']
            records = data['records']
            pageCount = data['pageCount']
            pageSize = data['pageSize']
            rowCount = data['rowCount']
            firstResult = data['firstResult']
            # print(len(records))
            print('pageCount=%s,pageSize=%s,rowCount=%s,firstResult=%s' % (pageCount, pageSize, rowCount, firstResult))
            order_list = []
            try:
                for record in records:
                    ordername = record['orderFlagcode'] if record['orderFlagcode'] else ""
                    order_info = {'factorynumber': record['woId'], 'ordername': ordername,
                                  'username': record['customerName'], 'mobile': record['customerPhone'],
                                  'orderstatus': '待派单', 'machinetype': record['productName'],
                                  'address': record['address'], 'ordertime': record['assignDate'],
                                  'repairtime': record['serviceDate'], 'description': record['reflectSituation'],
                                  'version': record['modelName'], 'sn': record['model'],
                                  'companyid': self.factoryid, 'machinebrand': '海尔', 'originname': 'CDK',
                                  'adminid': self.adminid}
                    order_list.append(order_info)
            except Exception as e:
                print(order_list)
                error = self.datafail.copy()
                error['msg'] = str(e)
                return error
            checkRes = requests.post(self.bjdomain + "/Api/Climborder/addorder", data={"data": json.dumps(order_list)})
            checkRes.encoding = 'utf-8'

            if checkRes and checkRes.status_code == 200:
                print("海尔工单同步成功")
                return self.datasuccess
        return self.datasuccess


if __name__ == '__main__':
    util = CDKCookieUtil('66004185', 'Dw147259', adminid='24', factoryid='18')
    print(util.loadOrders())
