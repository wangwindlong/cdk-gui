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
from cookie_test import fetch_chrome_cookie


class JDUtil:
    def __init__(self, adminid='24', factoryid='2222', baseurl='http://jdfw.jd.com',
                 bjdomain='http://fatest.bangjia.me'):
        parsed_uri = urlparse(baseurl)
        self.host = parsed_uri.netloc
        self.baseurl = baseurl
        self.adminid = adminid
        self.factoryid = factoryid
        self.bjdomain = bjdomain
        self.mainurl = self.baseurl + '/admin/page!main.action'
        self.searchurl = self.baseurl + '/receipt/query.json'
        self.cookie = fetch_chrome_cookie([{"domain": ".jd.com"}], isExact=False)
        # self.cookie = '__jdu=15822142358071336720677; shshshfpa=4cb610d9-d916-ed24-90ac-26170aa59905-1582214236; shshshfpb=dxacIi12p1xApuBdUnj4Zzw%3D%3D; __jdv=122270672|direct|-|none|-|1587581491593; pinId=qPNJYlIyFdr3K3B-AGeThA; pin=djd0755860394; unick=jd_djd0486; _tp=aCXahsTQbNDTlwsCIhPtnQ%3D%3D; _pst=djd0755860394; preAlpha=2.0.0; ipLoc-djd=2-2813-51976-0; areaId=2; PCSYCityID=CN_310000_310100_310104; __jda=122270672.15822142358071336720677.1582214236.1587953354.1587955669.16; __jdc=122270672; 3AB9D23F7A4B3C9B=JTSXKQXK7BUSY6MK36CKHJYFEZS6XKXYQJ56FG37H7VDCOLXLDJSLL4WZYQFXYPBSU2NQCGFFDSD3CAGULQAQ6GGNE; user-key=f717fb9f-52b2-4338-a979-e0f36a24be06; cn=3; shshshfp=63c9b8407561954dc36b1e1a960de1a1; wlfstk_smdl=2lv84hd4cptgniiti23gpi8nwnt4z7d1; TrackID=1a4qEw3PrfYzPrup5CAvYnyVpfundPVFS17nU3yojP1_B9tf_WHqhVYakJClrehbtoGqcXHcfZ8s5zJ3_-13WTFOYJIWv3hLfEk67uh2B8LQ; thor=76167CD23714F158A010161AB3D4AD0189D6C181A37C49C8A0B98C6B2AD8D4DF17D8CE83A72D770118159A439395D1FF76A6F33B62952ACA13628500648B136FB3CCE2939B1DB28AD0D3EF3396B9438379A94C15183CF589A921B6EB43C65F6AEA72E03273DD3BFC475777CE4EBCA17387DF867162100D53A5290625097A0D0DE6720F5651DE74FBBF3251A1C4E9C86C; ceshi3.com=000; shshshsID=e9fdc2803f82466948087f6d0fa60a57_3_1587955698712; __jdb=122270672.6.15822142358071336720677|16.1587955669'
        self.cookies = JDUtil.getCookies(self.cookie)
        self.session = requests.Session()
        self.agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
        self.datasuccess = {'code': 1, 'msg': '抓单成功', 'element': ''}
        self.datafail = {'code': 0, 'msg': '抓单失败,请使用谷歌浏览器登录京东账号后重试'}
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded',
                        'User-Agent': self.agent, 'Host': self.host, 'Origin': self.baseurl,
                        'Accept-Encoding': 'gzip, deflate', 'Cookie': self.cookie,
                        'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
        self.headers[
            'Referer'] = self.baseurl + '/receipt/receiptDashboardIndex?homePageDistinguish=notAppointed&serviceType=0'
        self.headers['Accept'] = '*/*'
        response = self.session.post(self.baseurl + "/common/inforLinkage/getPerson", headers=self.headers)
        response.encoding = 'utf-8'
        # print(response.text)
        if response.status_code == 200:
            return self.getOrgan(json.loads(response.text))
        return self.datafail

    def getOrgan(self, datas):
        response = self.session.post(self.baseurl + "/wareset/getImBaseLasWare", headers=self.headers,
                                     data={"lasWareCode": datas['wareHouseNo']})
        response.encoding = 'utf-8'
        # print(response.text)
        if response.status_code == 200:
            return self.loadMains(dict(datas, **(json.loads(response.text)[0])))
        return self.datafail

    def loadMains(self, datas):
        data = {
            # "esSwitch": "1", "subCompanyId": str(organdatas['mcustCode']),
            "esSwitch": "1", "subCompanyId": str(datas['mcustCode']),
            # "wareInfoId": str(organdatas['lasWareRelation'])
            "wareInfoId": str(datas['lasWareRelation']), "outletsId": str(datas['infoLink']),
            "sortKind": "4", "page": "1", "rows": "50", "reservationStatus": "3",  # 3 为未预约状态
            "sort": "returnTime", "order": "desc", "serviceType": "0", "fastDealNum": "5"  # 5为 待预约，7为待反馈
        }
        result = ""
        for item in data:
            result += item + "=" + data[item] + "&"
        result = result + "freeinstall=&startStatus=&endStatus=&timeout=&todayOtherReservationConditionName=&productBrand=&productType1=&productType2=&productType3=&orderId=&bizOrderId=&ordernoGroup=&customerName=&customerPhone=&serviceStreet=&wareId=&productName=&orderStatus=&orderStatusGroup=&createOrderTimeBegin=&createOrderTimeEnd=&reservationDateBegin=&reservationDateEnd=&firstReservationTimeBegin=&firstReservationTimeEnd=&changedReservationDateBegin=&changedReservationDateEnd=&feedbackStatus=&orderOrderStatus=&expectAtHomeDateBegin=&expectAtHomeDateEnd=&atHomeFinishDateBegin=&atHomeFinishDateEnd=&deliveryDateStart=&deliveryDateEnd=&homePageDistinguish=&fastDealNumByColor=&reportLessFlag=&superExperienceStore=&sourceOrderIdGroup=&sellerId=&sellerName=&eclpBusinessNo=&isFast="
        # print(result)
        params = {}
        datas = result.split("&")
        for data in datas:
            content = data.split("=")
            if len(content) > 1:
                params[content[0]] = content[1]
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        response = self.session.post(self.searchurl, headers=self.headers, data=params)
        response.encoding = 'utf-8'
        # print(response.url)
        # print(response.text)
        # print(response.headers)
        if response.status_code != 200 or "error" in response.url:
            print("请求{}失败，返回：{},请使用谷歌浏览器重新登录京东系统".format(response.url, response.text))
            return self.datafail
        return self.loadOrders(json.loads(response.text))

    def loadOrders(self, datas):
        try:
            data = {"data": json.dumps(self.parseOrders(datas))}
            requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
        except Exception as e:
            print("addorder failed:", e)
            return self.datafail
        return self.datasuccess

    def parseOrders(self, datas):
        if 'total' not in datas:
            return []
        total_num = datas['total']
        # print("total count:{}".format(total_num))
        order_list = []
        for order_key in datas['rows']:
            # reservationServiceTypeName ：安装  createOrderTime：1588123851000
            mobile = order_key['customerPin'].split("_")[0]
            order_info = {
                'factorynumber': order_key['orderId'], 'ordername': order_key['serviceTypeName'],
                'username': order_key['customerName'], 'mobile': mobile,
                'orderstatus': order_key['orderStatusName'], 'originname': '京东系统',
                'machinetype': order_key['productTypeName'], 'machinebrand': order_key['productBrandName'],
                'version': order_key['productName'], 'sn': order_key['wareId'],
                'companyid': self.factoryid, 'adminid': self.adminid,
                'address': str(order_key['serviceStreet']),
                'province': order_key['serviceProvince'], 'city': order_key['serviceCity'],
                'county': order_key['serviceCounty'], 'town': order_key['serviceDistrict'],
                'ordertime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(order_key['createOrderTime'] / 1000)),
                'repairtime': order_key['expectAtHomeDate'],
                'note': str(order_key['feedbackNote'] if order_key['feedbackNote'] else '') + str(
                    order_key['exceptionFeeApprovalStatusName'] if order_key['exceptionFeeApprovalStatusName'] else ''),
                'description': order_key['feedbackResult'],
            }
            order_list.append(JDUtil.clearAddress(order_info))
        return order_list

    @staticmethod
    def clearKey(data, datakey, destkey='address'):
        if datakey in data and data[datakey] in data[destkey]:
            data[destkey] = data[destkey].replace(data[datakey], '')
        return data

    @staticmethod
    def clearAddress(orderinfo):
        if "address" not in orderinfo:
            return orderinfo
        orderinfo = JDUtil.clearKey(orderinfo, "province")
        orderinfo = JDUtil.clearKey(orderinfo, "city")
        orderinfo = JDUtil.clearKey(orderinfo, "county")
        orderinfo = JDUtil.clearKey(orderinfo, "town")
        return orderinfo


if __name__ == '__main__':
    util = JDUtil('24', factoryid='222')
    print(util.loadMain())
