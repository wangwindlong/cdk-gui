import datetime
import json
import os
import re
import random
import sys
from urllib import parse
from urllib.parse import urlparse

import requests
from PIL import Image
from io import BytesIO

from bs4 import BeautifulSoup


# from useragent import agents


class CDKUtil:
    def __init__(self, username='', passwd='Dw147259', token=None):
        self.baseurl = "http://cdk.rrs.com"
        self.mainurl = 'http://cdk.rrs.com/manager-web/index.do'
        self.session = requests.Session()
        # self.agent = random.choice(agents)
        self.agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        self.guidStr = CDKUtil.guid()
        self.token = token
        self.orderurl = ''
        self.username = username
        self.passwd = passwd

    @staticmethod
    def guid():
        import uuid
        s_uuid = str(uuid.uuid4())
        l_uuid = s_uuid.split('-')
        s_uuid = ''.join(l_uuid)
        s_uuid = s_uuid[:12] + "4" + s_uuid[13:]
        return s_uuid

    def generateCode(self):
        self.guidStr = CDKUtil.guid()
        # 动态加载验证码图片
        captchaUrl = self.baseurl + "/login/generateCode?redisKey=" + self.guidStr
        print("generateCode guidStr=%s,captchaUrl=%s" % (self.guidStr, captchaUrl))
        response = self.session.get(captchaUrl)
        return Image.open(BytesIO(response.content))
        # _code = OCRUtil.getCode(img, config_cdk, tesseract_path)
        # print("generateCode captchaUrl: %s ,getCode :%s" % (captchaUrl, _code))

    # 校验验证码
    def checkCode(self, code, name, passwd):
        self.username = name
        self.passwd = passwd
        params = {"redisKey": self.guidStr, "checkCode": code}
        headers = {'content-type': 'application/json; charset=utf-8', 'X-Requested-With': 'XMLHttpRequest',
                   'User-Agent': self.agent,
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,pt;q=0.6', 'Connection': 'keep-alive',
                   'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8', 'Host': 'cdk.rrs.com'}
        checkRes = self.session.post(self.baseurl + "/login/checkCode", data=json.dumps(params), headers=headers)
        print('=========================checkCode')
        checkResult = json.loads(checkRes.text)
        # print(checkResult)

        # 验证码正确
        if checkResult and checkResult['result'] == '1':
            print("=========================验证成功")
            codeFaultTimes = 0
            return self.login(code, name, passwd)
        else:
            # 重新加载图片验证 验证码
            return False

    def login(self, code, username, passwd):
        # 校验通过，模拟登陆
        params = {"loginname": username, "loginpwd": passwd,
                  "returnUrl": "http://cdk.rrs.com/manager-web/index.do", "checkCode": code}
        r = self.session.post(self.baseurl + "/login", data=params)
        r.encoding = 'utf-8'
        # 登录成功进入主界面
        if r.status_code == 200:
            mainhtml = BeautifulSoup(r.text, features="lxml")
            # print(mainhtml)
            # print("=========================")
            # print(r.headers)
            return self.getHaierUrl(mainhtml)
            # 重定向到location
        elif r.status_code == 302:
            # location = r.headers.getheader('Location')
            location = r.headers['Location']
            if location:
                # testcdk(name=name, passwd=passwd, url=location)
                return False
        # testcdk(name=name, passwd=passwd, url=baseurl + "/login.html?ReturnUrl=" + mainurl)
        return False

    def getHaierUrl(self, soap):
        # haierSpan = mainhtml.find("div", {"id": "serviceDiv"}).span
        haierSpan = soap.find('span', text=re.compile('海尔安装'))
        print("+++++++++++++++++++++++++++++++getHaierUrl")
        print(haierSpan)
        if not haierSpan:
            # testcdk(name=name, passwd=passwd, url=mainurl + "?token=" + self.token)
            return False
        haierUrl = haierSpan['href']
        return self.loadHaier(haierUrl)

    # 加载海尔安装模块
    def loadHaier(self, url):
        session = requests.Session()
        print("loadHaier url=" + url)
        haierMain = session.get(url)
        if haierMain.status_code == 200:
            soap = BeautifulSoup(haierMain.text, features="lxml")
            soap.encoding = 'utf-8'
            # print(soap)
            # 返回3个js polyfills.c38c86ad444630494a92.bundle.js main.4b3d8dea306811e889d6.bundle.js
            # http://cdkaz.rrs.com/inline.1557c7584b9dbbbbbcec.bundle.js

            return self.authAndgetMenu(url)

            # haierUrl = soap.find('a', text=re.compile('服务处理'))['href']
            # orderMain = loadHaier(session, baseurl + haierUrl)
            # print(orderMain)
        else:
            return False

    # url = http://cdkaz.rrs.com/pages/cdkinstall/serveprocess?moduleCode=04&newTopWindow=true&token=168E4C1CDFF64967C3336A8ADF0CDB1B
    def authAndgetMenu(self, url):
        # 请求验证
        auth = 'http://cdkaz.rrs.com//api/system/authMenu/auth'
        parsed_url = urlparse(url)
        print("========----------=============")
        print(parsed_url)
        haierBaseUrl = parsed_url.scheme + "://" + parsed_url.netloc
        pageUrl = haierBaseUrl + parsed_url.path
        params = dict(parse.parse_qsl(parsed_url.query))
        self.token = params['token']  # 给全局变量赋值 token

        headers = {'content-type': 'application/json; charset=utf-8', 'X-Requested-With': 'XMLHttpRequest',
                   'User-Agent': self.agent,
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,pt;q=0.6', 'Connection': 'keep-alive',
                   'Accept': 'application/json, text/plain, */*', 'Host': parsed_url.netloc,
                   'Origin': haierBaseUrl}
        checkRes = self.session.post(auth, data=json.dumps(params), headers=headers)
        checkRes.encoding = 'utf-8'
        # print(checkRes.text)
        authResult = json.loads(checkRes.text)
        #  {token=168E4C1CDFF64967C3336A8ADF0CDB1B moduleCode=04 userId=''}
        if checkRes.status_code == 200 and authResult['success']:
            menuUrl = 'http://cdkaz.rrs.com//api/system/authMenu/authMenuChanges'
            menuRes = self.session.post(menuUrl, data=json.dumps(params), headers=headers)
            menuRes.encoding = 'utf-8'
            menuResult = json.loads(menuRes.text)
            # print("========----------=============")
            # print(menuRes.text)
            if menuRes.status_code == 200 and menuResult['success']:
                for data in menuResult['data']:
                    # print(data)
                    # print("========")
                    for children in data['children']:
                        for childitem in children['children']:
                            # print(childitem)
                            # print("-------")
                            if childitem['text'] == '服务处理':
                                self.orderurl = haierBaseUrl + childitem['link'] + "?" + str(parse.urlencode(params))
                                self.updateUser(self.username, self.passwd, self.orderurl)
                                return self.loadHaierOrder()
        return False  # 重新登录

    def loadHaierOrder(self):
        print("loadHaierOrder url=" + self.orderurl)
        parsed_url = urlparse(self.orderurl)
        apipath = '/api/businessData/serviceList/selectServiceDealList'
        print("***********************************")
        haierBaseUrl = parsed_url.scheme + "://" + parsed_url.netloc
        pageUrl = haierBaseUrl + apipath
        params = dict(parse.parse_qsl(parsed_url.query))
        today = datetime.date.today()  # 获得今天的日期
        params['jobStatus'] = '1#3'  # 只需要一种未派人状态 空则为全部， 1#3#4#5
        params['regTimeStart'] = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d %H:%M:%S')
        params['regTimeEnd'] = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        params['pageIndex'] = 1
        params['rows'] = 50
        headers = {'content-type': 'application/json',
                   'User-Agent': self.agent,
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,pt;q=0.6', 'Connection': 'keep-alive',
                   'Accept': 'application/json, text/plain, */*', 'Host': parsed_url.netloc,
                   'Origin': haierBaseUrl, 'Referer': self.orderurl}
        params = json.dumps(params)
        headers['Content-Length'] = str(len(params))
        print("loadHaierOrder params:")
        # print(params)
        # print(headers)
        orderRes = self.session.post(pageUrl, data=params, headers=headers)
        orderRes.encoding = 'utf-8'
        # print(orderRes.text)
        orderResult = json.loads(orderRes.text)
        if orderRes.status_code == 200 and orderResult['success'] and orderResult['data']:
            data = orderResult['data']
            records = data['records']
            pageCount = data['pageCount']
            pageSize = data['pageSize']
            rowCount = data['rowCount']
            firstResult = data['firstResult']
            print(len(records))
            print('pageCount=%s,pageSize=%s,rowCount=%s,firstResult=%s' % (pageCount, pageSize, rowCount, firstResult))
            new_datas = {}
            order_list = []
            for record in records:
                ordername = "安装" if "安装" in record['orderFlagcode'] else "维修"
                order_info = {'factorynumber': record['woId'], 'ordername': ordername,
                              'username': record['customerName'], 'mobile': record['customerPhone'],
                              'orderstatus': '待派单', 'machinetype': record['productName'],
                              'address': record['address'], 'ordertime': record['assignDate'],
                              'repairtime': record['serviceDate'], 'description': record['reflectSituation'],
                              'version': record['modelName'], 'sn': record['model'],
                              'companyid': 18, 'machinebrand': '海尔', 'originname': 'CDK', 'adminid': '26073'}
                order_list.append(order_info)
            checkRes = requests.post("http://north.bangjia.me/Api/Climborder/addorder",
                                     data={"data": json.dumps(order_list)})
            checkRes.encoding = 'utf-8'

            if checkRes and checkRes.status_code == 200:
                print("同步成功")
                return True
            # for record in records:
            #     new_datas[record['woId']] = Order(username=record['customerName'], orderno=record['woId'],
            #                                       originno=record['sourceCode'],
            #                                       mobile=record['customerPhone'], address=record['address'],
            #                                       machineversion=record['modelName'],
            #                                       data=json.dumps(record), token=token, uname=name)
            # for each in Order.query.filter(Order.orderno.in_(new_datas.keys())).all():
            #     # Only merge those posts which already exist in the database
            #     # data = new_datas.pop(list(new_datas.keys()).index(each.orderno))
            #     data = new_datas.pop(each.orderno, None)
            #     each.uname = name
            #     # print("data=" + str(data))
            #     # if data:
            #     #     print("data orderno=" + data.orderno)
            #     #     db.session.merge(data)
            #
            # # Only add those posts which did not exist in the database
            # db.session.add_all(new_datas.values())
            #
            # # Now we commit our modifications (merges) and inserts (adds) to the database!
            # db.session.commit()
        return False

    def updateUser(self, name, passwd, orderurl):
        userinfo = {"username": name, "passwd": passwd, "token": self.token, 'islogin': True, 'orderurl': orderurl}
        userfile = os.path.join(os.path.split(os.path.abspath(sys.argv[0]))[0], "file", "user.txt")
        with open(userfile, 'w') as f:
            jsObj = json.dumps(userinfo)
            f.write(jsObj)


if __name__ == '__main__':
    # util = JDUtil('24', factoryid='19')
    util = CDKUtil()
