import datetime
import json
import re
import random
import time
from urllib import parse

import requests
# from requests_html import HTMLSession

from useragent import agents


class MIUtil:
    def __init__(self, username='', passwd='',
                 cookie='uLocale=zh_CN; cUserId=9WoKEQRB9fVUADppwgOb3okY2Gk; _aegis_pp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1ODcwMzE4OTksImV4dHJhIjoicGFzc3BvcnQiLCJleHAiOjE1ODcxMjE4OTksImlzcyI6Ik1JLUlORk9TRUMiLCJhdWQiOiJ4bXMuYmUueGlhb21pLmNvbSIsInN1YiI6IjIxNTQ5MjkyODciLCJpYXQiOjE1ODcwMzE4OTl9.GIy1Q-ugPqvwuhHQxMbHnXeK7TjFJi7mebbY8yBTvrRspndUqRPkMTfVJnKPiQMRxNvxd-FCo_37KbdfO8SE6Q; serviceToken=zE1Q5iZtk7g4X4R3gVa2ChcBS4ERWuoytKRENXBg+KiYGW4bKs6wSnOcW6WQNxdBiW03U8XJ4Ml6Um5G5/wIVhGILk56f7lSZ5xhFElqy1E=; userId=2154929287; xmsbe_slh=7AiF/Y6OjzlZNYmOTPFqDnGxqeY=; localtimezone=28800; mstuid=1587031901233_5533; Hm_lvt_02f2b1424a5046f7ae2353645198ca13=1587031902; lastsource=account.xiaomi.com; JSESSIONID=ab5200eb-1f5c-46dd-942f-df8b9fddb72b; mstz=--%E6%9C%8D%E5%8A%A1%E5%8D%95%E6%9F%A5%E8%AF%A2%7C%7C2096194703.8%7C%7Chttps%253A%252F%252Faccount.xiaomi.com%252Fidentity%252Fauthstart%253Fsid%253Dpassport%257Ccontext%253Dhs28oywix%25252fcvay4u5ykuvptz34w8cid7chl%25252frws1i1y2s461gaz%25252f0crsvxlgjxlouzfdtaqxncodhiqhqm7snntq9dvlwh0y6ftiapnrh5paoivyfss1gh%25252fux8exzyvcaqbotr574%25252bn1qdllhqaiwwezxnuulkiptcld6lplhyly0j1p%25252b1qqm%25252fx1yp5uifnz0qjcvvmogscoplxyc842lbnel0ntmztyyfz5vakeyttkrx%25252f8%25252f4yc08u2vpld3morkd%25252b24bzuhgh03gvhj%25252f%25252fzf7hlf3iev9asw8rzett%25252fri%25252frvx1j%25252b2w5cckyudqkx2qqfya4q8amzs46yuiy0sdxhvgllwdoyc%25252f%25252b0%25252fz889rc25ckrrzfdo78prndjfbndlo8oycpjjhv8t3ikwvgsm11itcervcnj5exylcbqrw%25252b%25252bf1nfcnfo8l%25252fglria0ap79d9qakw%25252bortupf3b4nwuydrleohi5q2n6u6uhdo%25252fwygnfqja%25252fl3aqesvpj3rx23g7kxh%25252fpqsmawrsgdzicu4wm0ekj0stba0mbxylffopafjbeerdi5rpx70n0wdbpjlqhi8pk3ghywsfzwgxsebczdxrvkejsyoynfixpdnk8dfrfwc3dst69d4hieaywajvgi8nuzcaglesl2haxchrgbtpiev394kjqghne5qyqjkhakcufykva28tba8th7lsjal%25252f989yvicsvsfvz5gq4jsqrnc%25252bg%25252fbytovnscts5x1mx%25252b5xmf0jri0bczjqh2npdhw%25252b3%25252bhhuti6j0z8%25252bfu0nqkrwzailqkyhgtimcmhhiijlflji7vr1x3vs6e60v1tmhbqhe7gt52xnakvzk2x7hpr1qfjys7ayq8ev%25252bxb5ks4%25252bquugtla77yxfywnmt8scoqbacbg%25252fj6gmvi0jeje1nljhf24o21o%25252bcxjsgrx65tvuvknurmzm9hskye3qq66ho1czfcyfiu7sgpr1jfy7dj%25252fww6reqeypngsuc%25252f4k9ij2foy8vlowqmc0v8zedohoxdazyupybvle5iu7uhp%25252b83cwwg98v5g%25252beoc8kxhgbgvayiemf1pjizkbccfgunmvwxj665y29f91uo8l%25252bjkypjv7darjcdr2uiqgpxflfg89h2bqjfs5mna%25252fasb%25252bcm4q8%7C; xm_vistor=1587031901233_5533_1587110757076-1587110757076; Hm_lpvt_02f2b1424a5046f7ae2353645198ca13=1587110779; xst=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoxNTg3MTExMzU3LCJjdXRPcmdJZCI6IldEQ04wMjcwMiIsImV4cCI6MTU4NzExMzE1NywibWlsaWFvIjoyMTU0OTI5Mjg3LCJvcmdJZCI6IldEQ04wMjcwMiJ9.c-B4y_3nqvsTYjOHTUDS6QJAWztBCCjQkM2VqsGy5yo'):
        self.cookie = cookie
        self.cookies = MIUtil.getCookies(cookie)
        self.accounturl = 'https://account.xiaomi.com/pass/serviceLogin'
        self.host = 'xms.be.xiaomi.com'
        self.baseurl = "https://" + self.host
        self.mainurl = self.baseurl + '/admin/page!main.action'
        self.searchurl = self.baseurl + '/afterservice/afterservice!api.action'
        self.session = requests.Session()
        # self.session = HTMLSession()
        self.agent = random.choice(agents)
        self.username = username
        self.passwd = passwd
        self.datasuccess = {'code': 1, 'msg': '登录成功', 'element': ''}
        self.datafail = {'code': 0, 'msg': '登录失败,请检查账号密码是否正确'}
        # self.bjdomain = "http://north.bangjia.me"
        self.bjdomain = 'http://fatest.bangjia.me'
        self.headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
                        'Upgrade-Insecure-Requests': '1', 'Host': self.host, 'Origin': self.baseurl,
                        'Accept-Encoding': 'gzip, deflate, br', 'Cookie': self.cookie,
                        'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive',
                        'Accept': 'application/json, text/javascript, */*; q=0.01'}

    @staticmethod
    def getCookies(cookie):
        s = cookie.split("; ")
        cookies = {}
        for c in s:
            content = c.split("=")
            cookies[content[0]] = content[1]
        return cookies

    def loadMain(self):
        searchurl = self.searchurl + "?router=service_list"
        self.headers['Referer'] = self.mainurl
        response = self.session.get(searchurl, headers=self.headers)
        response.encoding = 'utf-8'
        orgId = re.findall(r"var orgId = \"(.+?)\"", response.text, re.S)[0]
        # originOrgId = re.findall(r"originOrgId: '(.+?)',", response.text, re.S)[0]
        originOrgId = orgId
        print(orgId)
        self.loadOrders({'orgId': orgId, "originOrgId": originOrgId})

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
        print(response.text)
        datas = json.loads(response.text)
        print(datas['result']['pageInfo']['total'])
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
        print("total count:{}".format(total_num))
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
                          'companyid': '9', 'machinebrand': '小米', 'originname': '小米系统', 'adminid': '3'}
            order_list.append(self.getDetail(order_info, order_key))
        return order_list
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


util = MIUtil('2250202702', 'CP6200002549')
util.loadMain()
