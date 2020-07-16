import json
import re
import time
from datetime import date, timedelta
from urllib import parse
from urllib.parse import urlencode, urlparse

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
        loginurl = self.baseurl + "/ases-web/main/homeServiceOrders/biSmgzbb.action"
        header = self.headers.copy()
        del header['Content-Type']
        del header['Origin']
        loginRes = self.session.get(loginurl, headers=header)
        url = loginRes.url
        print(url)
        return url if "guId" in url else None

    def loadMenu(self, param=None):
        # print("===================loadMenu")
        loginurl = self.baseurl + "/ases-web/main/menu/queryMenu.action?pId=FUN_18_02"
        self.headers['Accept'] = 'application/json, text/plain, */*'
        self.headers['Referer'] = self.baseurl + '/ases-web/index.html'
        menuRes = self.session.get(loginurl, headers=self.headers)
        # print(menuRes.headers)  # FUN_18_02_33 BI   FUN_18_02_04:改派工人管理
        # print(menuRes.text)

    def getUserinfo(self, param=None):
        # self.loadMenu()
        print("===================getUserinfo")
        loginurl = self.baseurl + "/ases-web/main/user/userInfo.action"
        self.headers['Accept'] = 'application/json, text/plain, */*'
        self.headers['Referer'] = self.baseurl + '/ases-web/index.html'
        print("headers=", self.headers)
        userRes = self.session.get(loginurl, headers=self.headers)
        print("userRes=", userRes.text)
        userinfo = self.getjson(userRes)
        print(userinfo)
        if userinfo and userinfo['result'] and userinfo['data']:
            wd = userinfo['data']['wd']
            supplierCode = userinfo['data']['supplierCode']
            userId = userinfo['data']['userId']
            companyCode = userinfo['data']['companyCode'][0]
            result = {"wd": wd, "supplierCode": supplierCode, "userId": userId, "companyCode": companyCode}
            return result
        return None

    def loadOrders(self, param=None):
        # print("=================================loadOrders")
        if not self.userinfo:
            self.userinfo = self.getUserinfo()
        if not self.userinfo:
            return self.datafail
        biurl = self.loadBI()
        if not biurl:
            return self.datafail
        parsed_uri = urlparse(biurl)
        tianyanbase = parsed_uri.scheme + "://" + parsed_uri.netloc
        url = tianyanbase + "/lbi-web-in/ww/visittrack/queryGrid.action"
        header = {'Content-Type': 'application/x-www-form-urlencoded',
                  'User-Agent': self.agent, 'Upgrade-Insecure-Requests': '1',
                  'Host': parsed_uri.netloc, 'Origin': tianyanbase, 'Cookie': self.cookie,
                  'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Accept': 'text/html, */*; q=0.01'}
        bires = self.session.get(biurl, headers=header)
        # print("bires=", bires.text)
        # print("bires header=", bires.headers)
        cookies = self.cookies.copy()
        for c in bires.cookies:
            cookies[c.name] = c.value
            # print(c.name, c.value)
        header['Referer'] = biurl
        header['Cookie'] = self.initCookie(cookies)
        orders = list(self.searchBI(url, header, 1))
        print("loadOrders result count=", len(orders))
        try:
            data = {"data": json.dumps(orders)}
            # print(data)
            requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
            self.loadGaipaiOrder()
        except:
            return self.dataverify
        return self.datasuccess

    def initCookie(self, cookies=None):
        if not cookies:
            return ""
        result = ""
        for cookie in cookies:
            result += cookie + "=" + cookies[cookie] + "; "
        return result[:-2]

    def searchBI(self, url, header, page=1, totalcount=100):
        params = {"wd": self.userinfo['wd'][0], "companyCode": self.userinfo['companyCode'],
                  "reservationStartDate": (date.today() - timedelta(days=1)).strftime("%Y%m%d"),
                  "reservationEndDate": (date.today() + timedelta(days=1)).strftime("%Y%m%d"),
                  "sapOrderType": "ZS01,ZS02,ZS03,ZS04,ZS06,ZS11,ZS12,ZS24",
                  "page": str(page), "pageSize": "10"
                  }
        # print("header['Cookie']=", header['Cookie'])
        biresult = self.session.post(url, headers=header, data=params)
        # print("url=", url, "biresult=", biresult.text)
        soup = self.getsoup(biresult)
        totalRe = re.findall(re.compile(r"(\d+)", re.S), soup.find("span", {"class": "total"}).text.strip())
        if totalRe and len(totalRe) > 0:
            totalcount = totalRe[0]
        try:
            pageCount = int(soup.find("input", {"id": "pageCount"})['value'])
        except:
            pageCount = 0
        resulttable = soup.find("table", {"class": "webtable"})
        isall = page + 1 > pageCount
        print("totalcount=", totalcount, "pageCount=", pageCount, "page=", page, "isall=", isall)
        if resulttable:
            yield from self.parseOrders2(resulttable.find_all("tr"), header['Referer'])
            if not isall:
                yield from self.searchBI(url, header, page + 1, totalcount)

    def parseOrders2(self, tr_list, biurl):
        for tr in tr_list:
            if tr.has_attr('class'):
                continue
            order = self.parseOrder(tr)
            if order:
                yield self.orderdetail(order, biurl)

    def parseOrder(self, tr):
        tablecolumns = tr.find_all("td")
        try:
            orderno_td = tablecolumns[0]
            addr = tablecolumns[14].text.strip().split(";")  # 0;安徽省;六安市;****
            orderitem = orderno_td.find("a")
            if orderitem:
                # 这个是元素的点击事件id，下一个页面需要用到
                data = {
                    "oid": re.findall(re.compile(r"[(]'(.*?)'[)]", re.S), orderitem["onclick"])[0],
                    'factorynumber': self.finda(orderno_td), 'originname': tablecolumns[16].text.strip(),
                    'username': tablecolumns[13].text.strip(), 'mobile': tablecolumns[15].text.strip(),
                    'ordername': tablecolumns[2].text.strip().replace("服务订单", ""),
                    'ordertime': tablecolumns[6].text.strip(), 'mastername': tablecolumns[23].text.strip(),
                    'province': addr[1] if len(addr) > 1 else "", 'city': addr[2] if len(addr) > 2 else "",
                    'companyid': self.factoryid, 'machinebrand': tablecolumns[9].text.strip().split("(")[0],
                    'machinetype': tablecolumns[8].text.strip(), 'version': tablecolumns[7].text.strip(),
                    # 'machinebrand': re.findall(re.compile(r"(.*?)[(].*?[)]", re.S), tablecolumns[9].text.strip())[0],
                    'orderstatus': tablecolumns[4].text.strip(), 'adminid': self.adminid}
                print("parseorder data=", data)
                return data # if self.isNew(data, self.bjdomain, self.adminid) else None
        except Exception as e:
            print("parseorder exception", e)
        return None

    def orderdetail(self, data, biurl):
        """获取到的是aes加密后的数据，暂未找到破解方法"""
        # url = self.baseurl + "/ases-web/main/external/bi/changeShow.action?orderId=" + data['oid']
        # header = self.headers.copy()
        # header['Referer'] = biurl
        # detailRes = self.session.get(url, headers=header)
        # print("detailRes=", detailRes.text)
        # print("detail url=", detailRes.url)
        return data

    def loadGaipaiOrder(self):
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
        gaipaiOrder = self.parseOrders(orderRes)
        """以下获取的es数据也为加密后的数据"""
        # print("orderRes.text=", orderRes.text)
        # esurl = self.baseurl + "/ases-web/main/ui/smOrder/queryListFromES.action"
        # self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        # self.headers['Accept-Encoding'] = 'gzip, deflate'
        # self.headers['Accept'] = 'application/json, text/plain, */*'
        # params = {"wd": self.userinfo['wd'][0], "companyCode": self.userinfo['companyCode'],
        #           "srvSaleCountStart": (date.today() - timedelta(days=3)).strftime("%Y-%m-%d"),
        #           "srvSaleCountEnd": (date.today() + timedelta(days=3)).strftime("%Y-%m-%d"),
        #           "createTimeStart": "", "createTimeEnd": "", "finishTimeStart": "", "finishTimeEnd": "",
        #           "orderId": "", "cmmdtyCtgry": "", "cityCodes": "", "mobPhoneNum": "",
        #           "page": "1", "pageSize": "100"
        #           }
        # print("esorder params=", params)
        # orderRes = self.session.post(esurl, headers=self.headers, data=params)
        # print("esorder orderRes.text=", orderRes.text)
        # ESOrder = self.parseOrders(orderRes)
        ESOrder = []
        try:
            data = {"data": json.dumps(gaipaiOrder + ESOrder)}
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
    # print(util.loadBI())
