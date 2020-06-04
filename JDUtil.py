import json
import re
import time

import requests
from BaseUtil import BaseUtil


class JDUtil(BaseUtil):
    def __init__(self, username='', passwd='', adminid='24', factoryid='19', baseurl='http://jdfw.jd.com',
                 bjdomain='http://yxgtest.bangjia.me'):
        super(JDUtil, self).__init__(username, passwd, adminid, factoryid, baseurl, bjdomain)
        self.mainurl = self.baseurl + '/admin/page!main.action'
        self.searchurl = self.baseurl + '/receipt/query.json'
        self.cookie = BaseUtil.getCookie([{"domain": ".jd.com"}])
        self.cookies = BaseUtil.getCookies(self.cookie)
        self.headers['Cookie'] = self.cookie
        self.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng," \
                                 "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    def loadMain(self):
        self.headers['Referer'] = self.baseurl + '/receipt/receiptDashboardIndex?homePageDistinguish=notAppointed'
        self.headers['Accept'] = '*/*'
        response = self.session.post(self.baseurl + "/common/inforLinkage/getPerson", headers=self.headers)
        response.encoding = 'utf-8'
        # print("loadMain result:{}".format(response.text))
        # print("=============================================")
        if response.status_code == 200:
            return self.getOrgan(json.loads(response.text))
        return self.datafail

    def getOrgan(self, datas):
        response = self.session.post(self.baseurl + "/wareset/getImBaseLasWare", headers=self.headers,
                                     data={"lasWareCode": datas['wareHouseNo']})
        response.encoding = 'utf-8'
        # print("getOrgan result:{}".format(response.text))
        # print("=============================================")
        if response.status_code == 200:
            return self.loadMains(dict(datas, **(json.loads(response.text)[0])))
        return self.datafail

    def uploadOrders(self, datas):
        try:
            data = {"data": json.dumps(datas)}
            # print("uploadOrders data={}".format(data))
            requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
        except Exception as e:
            print("addorder failed:", e)
            return self.datafail
        return self.datasuccess

    def loadMains(self, datas):
        result = []
        orders = self.loadPageOrders(datas, 0)
        if orders and "code" not in orders:
            result += orders
        orders = self.loadPageOrders(datas, 1)
        if orders and "code" not in orders:
            result += orders
        result += orders
        # print("loadMains result={}".format(result))
        # print("=============================================")
        return self.uploadOrders(result)

    def loadPageOrders(self, datas, serviceType):
        """ 抓取serviceType [0,1] 类型的所有单子"""
        data = {
            # "esSwitch": "1", "subCompanyId": str(organdatas['mcustCode']),
            "esSwitch": "1", "subCompanyId": str(datas['mcustCode']),
            # "wareInfoId": str(organdatas['lasWareRelation'])
            "wareInfoId": str(datas['lasWareRelation']), "outletsId": str(datas['infoLink']),
            "sortKind": "4", "page": "1", "rows": "50", "reservationStatus": "",  # 3 为未预约状态 空为所有状态
            "sort": "returnTime", "order": "desc", "serviceType": str(serviceType),  # 0为安维工单 1为售后工单
            "fastDealNum": "5"  # 5为 待预约，7为待反馈 0为所有状态
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
        self.headers['Referer'] = self.baseurl + '/receipt/receiptDashboardIndex?homePageDistinguish=notAppointed' \
                                                 '&serviceType=' + str(serviceType)
        response = self.session.post(self.searchurl, headers=self.headers, data=params)
        response.encoding = 'utf-8'
        # print(response.url)
        # print(response.text)
        # print(response.headers)
        if response.status_code != 200 or "error" in response.url:
            print("请求{}失败，返回：{},请使用谷歌浏览器重新登录京东系统".format(response.url, response.text))
            return self.dataverify
        return list(self.parseOrders(self.getjson(response)))

    def parseOrders(self, datas):
        if 'total' not in datas:
            return []
        total_num = datas['total']
        print("total count:{}".format(total_num))
        for data in datas['rows']:
            yield from self.parseOrder(data)

    def parseOrder(self, data):
        # reservationServiceTypeName ：安装  createOrderTime：1588123851000
        mobile = data['customerPin'].split("_")[0]
        brand = re.sub(r'（[^（）]*）', '', data['productBrandName'])
        orderno = "_{}".format(data['orderno']) if 'orderno' in data and data['orderno'] else ''
        order_info = {
            'factorynumber': data['orderId'] + orderno, 'ordername': data['serviceTypeName'],
            'username': data['customerName'], 'mobile': mobile,
            'orderstatus': data['orderStatusName'], 'originname': '京东系统',
            'machinetype': data['productTypeName'], 'machinebrand': brand,
            'version': data['productName'], 'sn': data['wareId'],
            'companyid': self.factoryid, 'adminid': self.adminid,
            'address': str(data['serviceStreet']),
            'province': data['serviceProvince'], 'city': data['serviceCity'],
            'county': data['serviceCounty'], 'town': data['serviceDistrict'],
            'ordertime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['createOrderTime'] / 1000)),
            'repairtime': data['expectAtHomeDate'],
            'note': str(data['feedbackNote'] if data['feedbackNote'] else '') + str(
                data['exceptionFeeApprovalStatusName'] if data['exceptionFeeApprovalStatusName'] else ''),
            'description': data['feedbackResult'] + " 安维单号：{}".format(data['orderno']),
            'ordernoSecret': data['ordernoSecret']
        }
        data = self.getUserInfo(JDUtil.clearAddress(order_info))
        # print(data)
        yield data

    def parseUserMobile(self, data, url, referer):
        header = self.headers.copy()
        header['Referer'] = referer
        response = self.session.get(url, headers=header)
        # print("parseUserMobile response:{}".format(response.text))
        if response.status_code != 200:
            return data
        bsObj = self.getsoup(response)
        tr = bsObj.find("form", {"id": "searchForm"}).find("tbody").find("tr")
        data['mobile'] = tr.find("input", {"name": "customerPhone"})["value"]
        return data

    def getUserInfo(self, data):
        if not data or "ordernoSecret" not in data:
            return data
        userurl = self.baseurl + "/receipt/manage?orderno=" + data['ordernoSecret']
        self.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng," \
                                 "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        response = self.session.get(userurl, headers=self.headers)
        # print("getUserInfo response:{}".format(response.text))
        if response.status_code != 200:
            return data
        bsObj = self.getsoup(response)
        iframe = bsObj.find("iframe", {"id": "innerframe"})
        if iframe:
            url = self.baseurl + str(iframe['src'])
            # parsed_url = urlparse(url)
            # params = dict(parse.parse_qsl(parsed_url.query))
            return self.parseUserMobile(data, url, userurl)
        return data


if __name__ == '__main__':
    # util = JDUtil('24', factoryid='19')
    util = JDUtil(adminid='1975', factoryid='19')
    print(util.loadMain())
