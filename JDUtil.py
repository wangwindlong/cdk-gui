import datetime
import json
import re
import time
from urllib import parse
from urllib.parse import urlparse

import requests
import httpx
from hyper.contrib import HTTP20Adapter
# from requests_html import HTMLSession
# from utils.ChromeCookie import fetch_chrome_cookie
# from cookie_test import fetch_chrome_cookie


class JDUtil:
    def __init__(self, adminid='24', factoryid='2222', baseurl='https://jdfw.jd.com',
                 bjdomain='http://north.bangjia.me'):
        parsed_uri = urlparse(baseurl)
        self.host = parsed_uri.netloc
        self.baseurl = baseurl
        self.adminid = adminid
        self.factoryid = factoryid
        self.bjdomain = bjdomain
        self.mainurl = self.baseurl + '/admin/page!main.action'
        self.searchurl = self.baseurl + '/receipt/query.json'
        # self.cookie = fetch_chrome_cookie([{"domain": ".xiaomi.com", "fields": ["mstz", "xst", 'uLocale']},
        #                                    {"domain": ".be.xiaomi.com", "fields": ["mstz", "xst", 'uLocale']},
        #                                    {"domain": "xms.be.xiaomi.com"},
        #                                    {"domain": ".xms.be.xiaomi.com"},
        #                                    {"domain": ".account.xiaomi.com"},
        #                                    {"domain": ".mi.com"}])
        self.cookie = '__jdu=15822142358071336720677; shshshfpa=4cb610d9-d916-ed24-90ac-26170aa59905-1582214236; shshshfpb=dxacIi12p1xApuBdUnj4Zzw%3D%3D; TrackID=1b9lbGbVU7O61Fr6HyapmMEc5hjyhdzGpWAScmasqi25g6DrtqgeYZIPpPHABo56YVms-jaaKjHEIMGaIrAIofEENuJ91AbELXGk9pRasOq2yFaZraAqCYfmkDnUBBGPl; 3AB9D23F7A4B3C9B=JTSXKQXK7BUSY6MK36CKHJYFEZS6XKXYQJ56FG37H7VDCOLXLDJSLL4WZYQFXYPBSU2NQCGFFDSD3CAGULQAQ6GGNE; shshshfp=15280c7c63c160a1bb26518b39131b5e; __jdv=122270672|direct|-|none|-|1587581491593; cid=NXRPNDE2NnFJNTU0N2NTMzMwOGxENzcwMXBNNDc4MnVXMDE2M3FBOTUwNGdWOTMw; __jda=122270672.15822142358071336720677.1582214236.1587581492.1587614898.13; __jdc=122270672; wlfstk_smdl=o2abs2bgsy6d17syw26rvwab1ph7zbmn; thor=76167CD23714F158A010161AB3D4AD0189D6C181A37C49C8A0B98C6B2AD8D4DFAC4822D5E358CAEE26981F439B73624D72257F1274D0B17EC3F7FD6A75D1D0D6090111C7C7178673686607C91C11875FA1AA045AD69183B271C143EB33734E3D0A248D93D963BB2A74CB5AF19A5A3DB0D42C66710C2F8E466CD095F14F2129689CBE7FC484FCA7E7ECD62751F8CF0ED3; pinId=qPNJYlIyFdr3K3B-AGeThA; pin=djd0755860394; unick=jd_djd0486; ceshi3.com=000; _tp=aCXahsTQbNDTlwsCIhPtnQ%3D%3D; logining=1; _pst=djd0755860394; preAlpha=2.0.0'
        self.cookies = JDUtil.getCookies(self.cookie)
        self.session = requests.Session()
        # self.session = HTMLSession()
        # self.agent = random.choice(agents)
        self.agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        self.datasuccess = {'code': 1, 'msg': '抓单成功', 'element': ''}
        self.datafail = {'code': 0, 'msg': '抓单失败,请使用谷歌浏览器登录京东账号后重试'}
        self.headers = {'content-type': 'application/x-www-form-urlencoded',
                        'User-Agent': self.agent,
                        'Upgrade-Insecure-Requests': '1', 'Host': self.host, 'Origin': self.baseurl,
                        'Accept-Encoding': 'gzip, deflate, br', 'Cookie': self.cookie,
                        'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        "X-Requested-With": "XMLHttpRequest",
                        "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin"
                        }
        # self.headers = JDUtil.authHeader(self.headers, self.host)

    @staticmethod
    def authHeader(header, host):
        header[':authority'] = host
        header[':method'] = 'POST'
        header[':path'] = '/receipt/query.json'
        header[':scheme'] = 'https'
        return header

    @staticmethod
    def getCookies(cookie):
        try:
            s = cookie.split("; ")
            cookies = {}
            for c in s:
                content = c.split("=")
                if len(content) > 1:
                    cookies[content[0]] = content[1]
            return cookies
        except Exception as e:
            print("getCookies", e)
            return ""

    def loadMain(self):
        # if 'userId' not in self.cookies:
        #     return self.datafail
        # 需要从页面获取： 运营中心：wareInfoId 分公司id：subCompanyIdHidden 网点简称：WebsiteInfoName  网点编码：outletsIdHidden
        data = {
            "esSwitch": "1", "subCompanyId": "10", "wareInfoId": "lw_10_334%%603_2", "outletsId": "0755860394",
            "sortKind": "4", "page": "1", "rows": "20", "sort": "returnTime", "order": "desc", "serviceType": "0",
            "fastDealNum": "5"
        }
        result = ""
        for item in data:
            result += item + "=" + data[item] + "&"
        result = result + "freeinstall=&startStatus=&endStatus=&timeout=&todayOtherReservationConditionName=&productBrand=&productType1=&productType2=&productType3=&orderId=&bizOrderId=&ordernoGroup=&customerName=&customerPhone=&serviceStreet=&wareId=&productName=&orderStatus=&orderStatusGroup=&createOrderTimeBegin=&createOrderTimeEnd=&reservationDateBegin=&reservationDateEnd=&firstReservationTimeBegin=&firstReservationTimeEnd=&changedReservationDateBegin=&changedReservationDateEnd=&feedbackStatus=&orderOrderStatus=&expectAtHomeDateBegin=&expectAtHomeDateEnd=&atHomeFinishDateBegin=&atHomeFinishDateEnd=&deliveryDateStart=&deliveryDateEnd=&homePageDistinguish=&fastDealNumByColor=&reservationStatus=&reportLessFlag=&superExperienceStore=&sourceOrderIdGroup=&sellerId=&sellerName=&eclpBusinessNo=&isFast="
        print(result)
        self.session.mount(self.baseurl, HTTP20Adapter())
        self.headers['Referer'] = self.baseurl + "receipt/receiptDashboardIndex?homePageDistinguish=notAppointed&serviceType=0"
        response = self.session.post(self.baseurl, headers=self.headers, data=result)
        # response = httpx.post(self.searchurl, headers=self.headers, data=data)
        response.encoding = 'utf-8'
        print(response.url)
        # orgIds = re.findall(r"var orgId = \"(.+?)\"", response.text, re.S)
        # datas = json.loads(response.text)
        print(response.text)
        print(response.headers)
        # if datas['code'] != 1 or not datas['result']:
        #     return self.datafail
        # orgIds = datas['result']
        # if not orgIds or len(orgIds) <= 0:
        #     return self.datafail
        # originOrgId = re.findall(r"originOrgId: '(.+?)',", response.text, re.S)[0]
        # orgId = orgIds[0]
        # orgId = orgIds[0]['id']
        # originOrgId = orgId
        # print(originOrgId)
        # return self.loadOrders({'orgId': orgId, "originOrgId": originOrgId})

    def loadOrders(self, param):
        self.headers['Referer'] = self.searchurl
        startTime = (datetime.date.today() + datetime.timedelta(days=-3)).strftime("%Y-%m-%d")
        endTime = (datetime.date.today() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
        params = {"key": "", "miliao": "", "curOperator": self.cookies['userId'], "originOrgId": param['originOrgId'],
                  "orgId": param['orgId'], "sId": "", "tel": "", "imei": "", "sn": "", "orderId": "",
                  "createStartTime": startTime, "createEndTime": endTime, "signStartTime": "", "signEndTime": "",
                  "closeStartTime": "", "closeEndTime": "", "returnStartTime": "", "returnEndTime": "",
                  "fullStartTime": startTime, "fullEndTime": endTime, "pageInfo": {"pageNum": 1, "pageSize": 100}}
        data = {'method': 'srvServicing.searchList',
                'params': json.dumps(params)}
        response = self.session.post(self.searchurl, data=parse.urlencode(data), headers=self.headers)
        response.encoding = 'utf-8'
        # print(response.text)
        datas = json.loads(response.text)
        # print(datas['result']['pageInfo']['total'])
        if datas['code'] == 1:
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
    util = JDUtil('24', factoryid='2222')
    print(util.loadMain())
