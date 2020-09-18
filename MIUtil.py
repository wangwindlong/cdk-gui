import datetime
import json
import re
import time
from urllib import parse
from urllib.parse import urlparse

import requests
# from requests_html import HTMLSession
# from utils.ChromeCookie import fetch_chrome_cookie
from BaseUtil import BaseUtil
from cookie_test import fetch_chrome_cookie


class MIUtil(BaseUtil):
    def __init__(self, adminid='68891', factoryid='17', baseurl='https://xms.be.xiaomi.com',
                 bjdomain='http://yxgtest.bangjia.me'):
        super(MIUtil, self).__init__('', '', adminid, factoryid, baseurl, bjdomain)
        parsed_uri = urlparse(baseurl)
        self.host = parsed_uri.netloc
        self.baseurl = baseurl
        self.adminid = adminid
        self.factoryid = factoryid
        self.bjdomain = bjdomain
        self.mainurl = self.baseurl + '/admin/page!main.action'
        self.searchurl = self.baseurl + '/afterservice/afterservice!api.action'
        self.cookie = fetch_chrome_cookie(
            [{"domain": ".xiaomi.com", "fields": ['uLocale', 'cUserId', 'userId', 'xmsbe_slh', "xst"]},
             {"domain": ".be.xiaomi.com", "fields": ["xst"]},
             {"domain": "xms.be.xiaomi.com"},
             {"domain": ".xms.be.xiaomi.com"},
             # {"domain": ".account.xiaomi.com"},
             # {"domain": ".mi.com"}
             ])
        # print(self.cookie)
        self.cookies = MIUtil.getCookies(self.cookie)
        self.session = requests.Session()
        # self.session = HTMLSession()
        # self.agent = random.choice(agents)
        self.agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/81.0.4044.113 Safari/537.36'
        self.datasuccess = {'code': 1, 'msg': '抓单成功', 'element': ''}
        self.datafail = {'code': 0, 'msg': '抓单失败,请使用谷歌浏览器登录小米账号后重试'}
        self.dataverify = {'code': 2, 'msg': '登录过期，请重新登录', 'element': ''}
        self.headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'User-Agent': self.agent,
                        'Upgrade-Insecure-Requests': '1', 'Host': self.host, 'Origin': self.baseurl,
                        'Accept-Encoding': 'gzip, deflate, br', 'Cookie': self.initCookie(self.cookies),
                        'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive',
                        'Accept': 'application/json, text/javascript, */*; q=0.01'}

    def initCookie(self, cookies=None):
        if not cookies:
            return ""
        result = ""
        for cookie in cookies:
            result += cookie + "=" + cookies[cookie] + "; "
        return result[:-2]

    def loadMain(self):
        if 'userId' not in self.cookies:
            return self.datafail
        # searchurl = self.searchurl + "?router=service_list"
        # data = "method=srvServicing.getJurisdictionOrg&params=" + self.cookies['userId']
        # print(data)
        self.headers['Referer'] = self.mainurl + "?"
        # print(self.headers['Cookie'])
        # print("***********************************")
        headers = self.headers.copy()
        headers[
            'Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        response = self.session.get(self.searchurl + "?router=service_list", headers=headers)
        response.encoding = 'utf-8'
        # print(response.headers['Set-Cookie'])
        # orgIds = re.findall(r"var orgId = \"(.+?)\"", response.text, re.S)
        # datas = json.loads(response.text)
        # print(response.text)
        result = re.findall(re.compile(r"originOrgId: ['](.*?)[']", re.S), response.text)
        if not result or len(result) == 0:
            return self.datafail
        orgId = result[0]
        # originOrgId = re.findall(r"originOrgId: '(.+?)',", response.text, re.S)[0]
        originOrgId = orgId
        # print(originOrgId)
        return self.loadOrders({'orgId': orgId, "originOrgId": originOrgId})

    def loadOrders(self, param=None):
        self.headers['Referer'] = self.searchurl
        # print(self.headers['Cookie'])
        # print("===============")
        startTime = (datetime.date.today() + datetime.timedelta(days=-3)).strftime("%Y-%m-%d")
        endTime = (datetime.date.today() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
        params = {"key": "", "miliao": "", "curOperator": self.cookies['userId'], "originOrgId": param['originOrgId'],
                  "orgId": param['orgId'], "sId": "", "tel": "", "imei": "", "sn": "", "orderId": "",
                  "createStartTime": startTime, "createEndTime": endTime, "signStartTime": "", "signEndTime": "",
                  "closeStartTime": "", "closeEndTime": "", "returnStartTime": "", "returnEndTime": "",
                  "fullStartTime": startTime, "fullEndTime": endTime, "pageInfo": {"pageNum": 1, "pageSize": 150}}
        data = {'method': 'srvServicing.searchList',
                'params': json.dumps(params)}
        response = self.session.post(self.searchurl, data=parse.urlencode(data), headers=self.headers)
        response.encoding = 'utf-8'
        # print("===================================loadOrders")
        # print(response.text)
        datas = json.loads(response.text)
        # print(datas['result']['pageInfo']['total'])
        if datas['code'] == 1:
            try:
                data = {"data": json.dumps(list(self.parseOrders(datas)))}
                # print("data=", data)
                requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
            except Exception as e:
                print(str(e))
                return self.datafail
            return self.datasuccess
        return self.datafail

    def parseOrders(self, datas):
        total_num = datas['result']['pageInfo']['total']
        # print("total count:{}".format(total_num))
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
            yield from self.getDetail(order_info, order_key)

    # 查询详情接口
    def getDetail(self, order, datas):
        self.headers['Referer'] = self.mainurl
        post_data = "method=srvServicing.getCommonSrvDetail&params=%7B%22sId%22%3A%22" + datas['sId'] + \
                    "%22%2C%22conditions%22%3A%22BASEINFO%22%7D"
        response = self.session.post(self.searchurl, data=post_data, headers=self.headers)
        response.encoding = 'utf-8'
        json_ret2 = json.loads(response.text)
        # print("===================================getDetail result")
        # print(response.text)
        if json_ret2['code'] == 1:
            datas['addressDescC'] = json_ret2['result']['baseInformation']['addressDescC']
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
        yield from self.showMsg(order, datas)

    def showMsg(self, order, datas):
        show_url = self.baseurl + '/common/common!savePrivateLogOperate.action'
        post_data = {"content": json.dumps({"miliao": [], "name": [datas['customerNameC']],
                                            "tel": [datas['customerTelC']],
                                            "email": [], "address": [datas['addressDescC']],
                                            "operateKey": datas['sId']})}
        response = self.session.post(show_url, data=post_data, headers=self.headers)
        response.encoding = 'utf-8'
        json_msg = json.loads(response.text)
        # print("===================================showMsg result")
        # print(response.text)
        if 'result' in json_msg:
            order['username'] = json_msg['result']['name'][0]
            order['mobile'] = json_msg['result']['tel'][0]
            order['address'] = json_msg['result']['address'][0]
        yield self.getDescription(order, datas)

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
    # util = MIUtil('20845', factoryid='17')
    util = MIUtil('24', factoryid='17', bjdomain='http://yxgtest.bangjia.me')
    print(util.loadMain())
