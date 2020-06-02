import datetime
import json
import re
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
        self.cdkbaseurl = ''
        self.cdkhost = ''

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
        print(self.cookie)
        if not self.islogin():
            return self.dataverify
        return self.loadHaierOrder()

    def islogin(self):
        url = self.baseurl + "/manager-web/index.do"
        header = self.headers.copy()
        header[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        # header['Referer'] = self.baseurl
        response = self.session.get(url, headers=header)
        soup = self.getsoup(response)
        # print(soup)
        haierSpan = soup.find('span', text=re.compile('海尔安装'))
        print("+++++++++++++++++++++++++++++++getHaierUrl")
        print(haierSpan)
        if not haierSpan:
            return False
        parsed_url = urlparse(haierSpan['href'])
        self.cdkhost = parsed_url.netloc
        self.cdkbaseurl = parsed_url.scheme + "://" + parsed_url.netloc
        params = dict(parse.parse_qsl(parsed_url.query))
        if 'token' in params:
            self.cookies['token'] = params['token']
            return True
        return False

    def loadHaierOrder(self):
        apipath = '/api/businessData/serviceList/selectServiceDealList'
        # print("***********************************loadHaierOrder")
        pageUrl = self.cdkbaseurl + apipath
        # params = dict(parse.parse_qsl(parsed_url.query))
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
        header['Cookie'] = 'ckbean=0'
        header['Host'] = self.cdkhost
        header['Origin'] = self.cdkbaseurl
        # print("loadHaierOrder params:")
        # print("params=", params)
        # print("header=", header)
        # print("pageUrl=", pageUrl)
        orderRes = self.session.post(pageUrl, data=params, headers=header)
        print(orderRes.text)
        orderResult = self.getjson(orderRes)
        if orderRes.status_code == 200 and orderResult['success'] and orderResult['data']:
            data = orderResult['data']
            records = data['records']
            pageCount = data['pageCount']
            pageSize = data['pageSize']
            rowCount = data['rowCount']
            firstResult = data['firstResult']
            print(len(records))
            print('pageCount=%s,pageSize=%s,rowCount=%s,firstResult=%s' % (pageCount, pageSize, rowCount, firstResult))
            order_list = []
            try:
                for record in records:
                    ordername = "安装" if "安装" in record['orderFlagcode'] else "维修"
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
                print("同步成功")
                return self.datasuccess
        return self.datafail


if __name__ == '__main__':
    util = CDKCookieUtil('66004185', 'Dw147259', adminid='24', factoryid='18')
    print(util.loadOrders())
