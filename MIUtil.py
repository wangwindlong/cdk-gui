import datetime
import json
import os
import re
import random
import sys
from urllib import parse
from urllib.parse import urlparse

import requests
# from requests_html import HTMLSession
from PIL import Image
from io import BytesIO

from bs4 import BeautifulSoup

from useragent import agents


class MIUtil:
    def __init__(self, username='', passwd='',
                 cookie='uLocale=zh_CN; cUserId=9WoKEQRB9fVUADppwgOb3okY2Gk; _aegis_pp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1ODcwMzE4OTksImV4dHJhIjoicGFzc3BvcnQiLCJleHAiOjE1ODcxMjE4OTksImlzcyI6Ik1JLUlORk9TRUMiLCJhdWQiOiJ4bXMuYmUueGlhb21pLmNvbSIsInN1YiI6IjIxNTQ5MjkyODciLCJpYXQiOjE1ODcwMzE4OTl9.GIy1Q-ugPqvwuhHQxMbHnXeK7TjFJi7mebbY8yBTvrRspndUqRPkMTfVJnKPiQMRxNvxd-FCo_37KbdfO8SE6Q; serviceToken=zE1Q5iZtk7g4X4R3gVa2ChcBS4ERWuoytKRENXBg+KiYGW4bKs6wSnOcW6WQNxdBiW03U8XJ4Ml6Um5G5/wIVhGILk56f7lSZ5xhFElqy1E=; userId=2154929287; xmsbe_slh=7AiF/Y6OjzlZNYmOTPFqDnGxqeY=; JSESSIONID=ee5d0651-2f44-46a0-a7c3-7f7edf395f03; localtimezone=28800; mstuid=1587031901233_5533; Hm_lvt_02f2b1424a5046f7ae2353645198ca13=1587031902; lastsource=account.xiaomi.com; mstz=--%E6%9C%8D%E5%8A%A1%E5%8D%95%E6%9F%A5%E8%AF%A2%7C%7C2096194703.2%7C%7Chttps%253A%252F%252Faccount.xiaomi.com%252Fidentity%252Fauthstart%253Fsid%253Dpassport%257Ccontext%253Dhs28oywix%25252fcvay4u5ykuvptz34w8cid7chl%25252frws1i1y2s461gaz%25252f0crsvxlgjxlouzfdtaqxncodhiqhqm7snntq9dvlwh0y6ftiapnrh5paoivyfss1gh%25252fux8exzyvcaqbotr574%25252bn1qdllhqaiwwezxnuulkiptcld6lplhyly0j1p%25252b1qqm%25252fx1yp5uifnz0qjcvvmogscoplxyc842lbnel0ntmztyyfz5vakeyttkrx%25252f8%25252f4yc08u2vpld3morkd%25252b24bzuhgh03gvhj%25252f%25252fzf7hlf3iev9asw8rzett%25252fri%25252frvx1j%25252b2w5cckyudqkx2qqfya4q8amzs46yuiy0sdxhvgllwdoyc%25252f%25252b0%25252fz889rc25ckrrzfdo78prndjfbndlo8oycpjjhv8t3ikwvgsm11itcervcnj5exylcbqrw%25252b%25252bf1nfcnfo8l%25252fglria0ap79d9qakw%25252bortupf3b4nwuydrleohi5q2n6u6uhdo%25252fwygnfqja%25252fl3aqesvpj3rx23g7kxh%25252fpqsmawrsgdzicu4wm0ekj0stba0mbxylffopafjbeerdi5rpx70n0wdbpjlqhi8pk3ghywsfzwgxsebczdxrvkejsyoynfixpdnk8dfrfwc3dst69d4hieaywajvgi8nuzcaglesl2haxchrgbtpiev394kjqghne5qyqjkhakcufykva28tba8th7lsjal%25252f989yvicsvsfvz5gq4jsqrnc%25252bg%25252fbytovnscts5x1mx%25252b5xmf0jri0bczjqh2npdhw%25252b3%25252bhhuti6j0z8%25252bfu0nqkrwzailqkyhgtimcmhhiijlflji7vr1x3vs6e60v1tmhbqhe7gt52xnakvzk2x7hpr1qfjys7ayq8ev%25252bxb5ks4%25252bquugtla77yxfywnmt8scoqbacbg%25252fj6gmvi0jeje1nljhf24o21o%25252bcxjsgrx65tvuvknurmzm9hskye3qq66ho1czfcyfiu7sgpr1jfy7dj%25252fww6reqeypngsuc%25252f4k9ij2foy8vlowqmc0v8zedohoxdazyupybvle5iu7uhp%25252b83cwwg98v5g%25252beoc8kxhgbgvayiemf1pjizkbccfgunmvwxj665y29f91uo8l%25252bjkypjv7darjcdr2uiqgpxflfg89h2bqjfs5mna%25252fasb%25252bcm4q8%7C; xm_vistor=1587031901233_5533_1587031901234-1587032541448; msttime=https%253A%252F%252Fxms.be.xiaomi.com%252Fadmin%252Fpage!main.action; msttime1=https%253A%252F%252Fxms.be.xiaomi.com%252Fadmin%252Fpage!main.action; xst=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoxNTg3MDMyNTU3LCJjdXRPcmdJZCI6IldEQ04wMjcwMiIsImV4cCI6MTU4NzAzNDM1NywibWlsaWFvIjoyMTU0OTI5Mjg3LCJvcmdJZCI6IldEQ04wMjcwMiJ9.mL-UjpX3F08IawzeSChHyGnvG3fonGFoqtHEfn_U5bA; Hm_lpvt_02f2b1424a5046f7ae2353645198ca13=1587032558 '):
        self.cookie = cookie
        self.cookies = MIUtil.getCookies(cookie)
        self.accounturl = 'https://account.xiaomi.com/pass/serviceLogin'
        self.host = 'xms.be.xiaomi.com'
        self.baseurl = "https://" + self.host
        self.mainurl = self.baseurl + '/admin/page!main.action'
        self.session = requests.Session()
        # self.session = HTMLSession()
        self.agent = random.choice(agents)
        self.orderurl = ''
        self.username = username
        self.passwd = passwd
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
        searchurl = self.baseurl + "/afterservice/afterservice!api.action?router=service_list"
        self.headers['Referer'] = self.mainurl
        response = self.session.get(searchurl, headers=self.headers)
        response.encoding = 'utf-8'
        # print(response.text)
        orgId = re.findall(r"orgId = \"(.+?)\"", response.text, re.S)[0]
        originOrgId = re.findall(r"originOrgId: '(.+?)'", response.text, re.S)[0]
        print(orgId, originOrgId)
        self.loadOrders({'orgId': orgId, "originOrgId": originOrgId})

    def loadOrders(self, param):
        searchurl = self.baseurl + "/afterservice/afterservice!api.action"
        self.headers['Referer'] = searchurl
        startTime = (datetime.date.today() + datetime.timedelta(days=-3)).strftime("%Y-%m-%d")
        endTime = (datetime.date.today() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
        params = {"key": "", "miliao": "", "curOperator": self.cookies['userId'], "originOrgId": param['originOrgId'],
                  "orgId": param['orgId'], "sId": "", "tel": "", "imei": "", "sn": "", "orderId": "",
                  "createStartTime": startTime, "createEndTime": endTime, "signStartTime": "", "signEndTime": "",
                  "closeStartTime": "", "closeEndTime": "", "returnStartTime": "", "returnEndTime": "",
                  "fullStartTime": startTime, "fullEndTime": endTime, "pageInfo": {"pageNum": 1, "pageSize": 100}}
        data = {'method': 'srvServicing.searchList',
                'params': json.dumps(params)}
        response = self.session.post(searchurl, data=parse.urlencode(data), headers=self.headers)
        response.encoding = 'utf-8'
        print(response.text)

    # def authLogin(self, params):
    #     r = self.session.get(url)
    #     r.encoding = 'utf-8'
    #     print(r.text)


util = MIUtil('2250202702', 'CP6200002549')
util.loadMain()
