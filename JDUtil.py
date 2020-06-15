import json
import os
import re
import sys
import time

import requests
from hyper.tls import init_context

from BaseUtil import BaseUtil
from hyper import HTTPConnection, HTTP20Connection

businessTypes = {"1": "上门安装", "2": "送货服务", "3": "提货送装", "4": "拆卸包装", "5": "退货服务"}
statusTypes = {"1": "新订单", "2": "自动分配失败", "3": "已分配", "4": "申请改派", "5": "已接收", "6": "已预约", "7": "已派工",
               "8": "上门完成", "12": "确认完成", "13": "取消服务", "14": "确认取消服务", "15": "客户取消"}


class JDUtil(BaseUtil):
    def __init__(self, username='', passwd='', adminid='24', factoryid='19', baseurl='http://jdfw.jd.com',
                 bjdomain='http://yxgtest.bangjia.me'):
        super(JDUtil, self).__init__(username, passwd, adminid, factoryid, baseurl, bjdomain)
        self.mainurl = self.baseurl + '/admin/page!main.action'
        self.searchurl = self.baseurl + '/receipt/query.json'
        self.popurl = "https://opn.jd.com/bill/query.json"
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
        print("loadMain result:{}".format(response.text))
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

    def mergeData(self, result, orders):
        if orders and "code" not in orders:
            result += orders
        return result

    def loadMains(self, datas):
        result = []
        result = self.mergeData(result, self.loadPageOrders(datas, 0))
        result = self.mergeData(result, self.loadPageOrders(datas, 1))
        self.uploadOrders(result)
        time.sleep(1)
        result = []
        result = self.mergeData(result, self.loadPageOrders(datas, 3))
        time.sleep(1)
        result = self.mergeData(result, self.loadPageOrders(datas, 4))
        # print("loadMains result={}".format(result))
        # print("=============================================")
        return self.uploadOrders(result)

    def ispop(self, serviceType):
        return serviceType == 3 or serviceType == 4

    def loadPopOrder(self, data, serviceType):
        result = ""
        for item in data:
            result += item + "=" + data[item] + "&"
        result = result[:-1]
        # 修改路径
        realpath = os.path.dirname(os.path.realpath(sys.argv[0]))
        print("realpath>>>>", realpath)
        cafile = os.path.join(realpath, "resource", 'pem', "certs.pem")
        print("cert_loc cafile>>>", cafile)
        conn = HTTP20Connection(host='opn.jd.com', port=443, ssl_context=init_context(cafile))

        headers = self.headers.copy()
        headers['Referer'] = "https://opn.jd.com/bill/search?billStatus=5"
        headers['Host'] = "opn.jd.com"
        headers['Origin'] = "https://opn.jd.com"
        headers[':authority'] = 'opn.jd.com'
        headers[':method'] = 'POST'
        headers[':path'] = '/bill/query.json'
        headers[':scheme'] = 'https'
        response = conn.request(method='POST', url=self.popurl, body=result, headers=headers)
        resp = conn.get_response(response)
        if resp.status != 200:
            print("请求{}失败，返回：{},请使用谷歌浏览器重新登录京东系统".format(response.url, response.text))
            return self.dataverify
        res = resp.read()
        # print(res)
        return list(self.parseOrders(json.loads(res), serviceType))

    def loadPageOrders(self, datas, serviceType):
        """ 抓取serviceType [0,1] 类型的所有单子 # 0为安维工单 1为售后工单 3为POP服务单 4为POP家具服务单"""
        data = {
            "sort": "returnTime" if not self.ispop(serviceType) else "billId", "order": "desc",
            "sortKind": "4", "page": "1", "rows": "500", "reservationStatus": "",  # 3 为未预约状态 空为所有状态
        }
        if self.ispop(serviceType):
            data['isAppliance'] = '1' if serviceType == 3 else '0'
            data['billStatuses'] = '5'
            data['isEgBuy'] = '0'
            data['outletsNo'] = str(datas['infoLink'])
            return self.loadPopOrder(data, serviceType)
        else:
            data['serviceType'] = str(serviceType)
            data['fastDealNum'] = '5'  # 5为 待预约，7为待反馈 0为所有状态
            data['esSwitch'] = '1'
            data['subCompanyId'] = str(datas['orgNo'])
            data['wareInfoId'] = str(datas['lasWareRelation'])
            data['outletsId'] = str(datas['infoLink'])

        result = ""
        for item in data:
            result += item + "=" + data[item] + "&"
        result = result + "freeinstall=&startStatus=&endStatus=&timeout=&todayOtherReservationConditionName=&productBrand=&productType1=&productType2=&productType3=&orderId=&bizOrderId=&ordernoGroup=&customerName=&customerPhone=&serviceStreet=&wareId=&productName=&orderStatus=&orderStatusGroup=&createOrderTimeBegin=&createOrderTimeEnd=&reservationDateBegin=&reservationDateEnd=&firstReservationTimeBegin=&firstReservationTimeEnd=&changedReservationDateBegin=&changedReservationDateEnd=&feedbackStatus=&orderOrderStatus=&expectAtHomeDateBegin=&expectAtHomeDateEnd=&atHomeFinishDateBegin=&atHomeFinishDateEnd=&deliveryDateStart=&deliveryDateEnd=&homePageDistinguish=&fastDealNumByColor=&reportLessFlag=&superExperienceStore=&sourceOrderIdGroup=&sellerId=&sellerName=&eclpBusinessNo=&isFast="
        # print("loadPageOrders requesturl=", result)
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
        url = self.searchurl if not self.ispop(serviceType) else self.popurl
        response = self.session.post(url, headers=self.headers, data=params)
        response.encoding = 'utf-8'
        # print(response.url)
        # print(response.text)
        # print(response.headers)
        if response.status_code != 200 or "error" in response.url:
            print("请求{}失败，返回：{},请使用谷歌浏览器重新登录京东系统".format(response.url, response.text))
            return self.dataverify
        return list(self.parseOrders(self.getjson(response), serviceType))

    def parseOrders(self, datas, serviceType):
        if 'total' not in datas:
            return []
        total_num = datas['total']
        print("total count:{}".format(total_num))
        for data in datas['rows']:
            yield from self.parseOrder(data, serviceType)

    def getordername(self, data, serviceType):
        if self.ispop(serviceType) and 'businessType' in data and data['businessType']:
            index = str(int(data['businessType']))
            return businessTypes[index] if index in businessTypes else ''
        elif not self.ispop(serviceType) and 'reservationServiceTypeName' in data:
            return data['reservationServiceTypeName'] if data['reservationServiceTypeName'] else ''

    def parseOrder(self, data, serviceType):
        # reservationServiceTypeName ：安装  createOrderTime：1588123851000
        mobile = str(data['customerPhone']) if 'customerPhone' in data else ''
        address = str(data['serviceStreet']) if 'serviceStreet' in data else data['customerAddress']
        address = address.replace("，", "").replace(",", "") if address else ''
        brand = re.sub(r'（[^（）]*）', '', data['productBrandName'])
        createTimeKey = "createOrderTime" if 'createOrderTime' in data else "createTime"
        orderid = "orderno" if not self.ispop(serviceType) else "billNo"
        orderno = "_{}".format(data[orderid]) if orderid in data and data[orderid] else ''
        ps = (" 安维单号：{}" if serviceType != 1 else " 售后单号：{}").format(data[orderid])
        if 'expectAtHomeDate' in data:
            repairtime = data['expectAtHomeDate']
        elif 'reservationInstallTime' in data and data['reservationInstallTime']:
            repairtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['reservationInstallTime'] / 1000))
        else:
            repairtime = ''
        order_info = {
            'factorynumber': (data['orderId'] if 'orderId' in data else data['orderid']) + orderno,
            'ordername': self.getordername(data, serviceType),
            'username': data['customerName'], 'mobile': mobile, 'originname': '京东系统',
            'orderstatus': data['orderStatusName'] if 'orderStatusName' in data else statusTypes["5"],
            'machinetype': data['productTypeName'] if 'productTypeName' in data else data['productCategoryName'],
            'machinebrand': brand,  'version': data['productName'],
            'sn': data['wareId'] if 'wareId' in data else data['productSku'],
            'companyid': self.factoryid, 'adminid': self.adminid, 'address': address,
            'province': data['serviceProvince'] if 'serviceProvince' in data else data['provinceName'],
            'city': data['serviceCity'] if 'serviceCity' in data else data['cityName'],
            'county': data['serviceCounty'] if 'serviceCounty' in data else data['districtName'],
            'town': data['serviceDistrict'] if 'serviceDistrict' in data else data['streetName'],
            'ordertime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data[createTimeKey] / 1000)),
            'repairtime': repairtime,
            'note': str(data['feedbackNote'] if 'feedbackNote' in data else data['saleFrom']) + str(
                data['exceptionFeeApprovalStatusName'] if 'exceptionFeeApprovalStatusName' in data else ''),
            'description': str(data['feedbackResult'] if 'feedbackResult' in data else data['reservationFailReason']) + ps,
            'ordernoSecret': data['ordernoSecret'] if 'ordernoSecret' in data else data['businessNo']
        }
        order_info = JDUtil.clearAddress(order_info)
        if not self.ispop(serviceType):
            order_info = self.getUserInfo(order_info)
        # print(order_info)
        yield order_info

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
    util = JDUtil(adminid='24', factoryid='19')
    # util = JDUtil(adminid='69046', factoryid='19')
    print(util.loadMain())
