import json
from datetime import date, timedelta
from urllib import parse

import requests
from bs4 import BeautifulSoup

from BaseUtil import BaseUtil
from cookie_test import fetch_chrome_cookie


class TCSMUtil(BaseUtil):

    def __init__(self, username, passwd, adminid='24', factoryid='6', baseurl='http://hk2.koyoo.cn/',
                 bjdomain='http://yxgtest.bangjia.me'):
        super(TCSMUtil, self).__init__(username, passwd, adminid, factoryid, baseurl, bjdomain)

        self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        self.dataverify = {'code': 2, 'msg': '登录过期，请重新登录', 'element': ''}
        self.cookie = fetch_chrome_cookie([{"domain": ".koyoo.cn"}], isExact=False)
        # self.cookie = 'lang=zh-cn; theme=default; sid=9b9is39q3gul5nrkrn4oo7n0d3'
        self.cookies = BaseUtil.getCookies(self.cookie)
        self.headers['Cookie'] = self.cookie
        self.headers['Accept-Encoding'] = 'gzip, deflate'
        self.skills = []

    def login(self, param=None):

        pass

    def islogin(self):
        self.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng," \
                                 "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        self.headers['Referer'] = self.baseurl + 'index.php?m=index&f=index'
        url = self.baseurl + "index.php?m=workorder&f=handleIndex"
        response = self.session.get(url, headers=self.headers)
        bsObj = self.getsoup(response)
        skillselect = bsObj.find("select", {"id": "skill"})

        if skillselect:
            skills = skillselect.find_all('option')
            self.skills = skills
            print(self.skills)
            return skills is not None
        else:
            return False

    def loadOrders(self, param=None):
        if not self.islogin():
            print("loadOrders is not login")
            return self.datafail
        self.headers['Accept'] = "application/json, text/javascript, */*; q=0.01"
        self.headers['Content-Type'] = 'application/json'
        try:
            data = {"data": json.dumps(self.loadOrderbySkill())}
            requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
        except:
            return self.datafail
        return self.datasuccess

    def loadOrderbySkill(self):
        print("loadOrderbySkill skills={}".format(self.skills))
        results = []
        for skill in self.skills:
            print("loadOrderbySkill skill={}".format(skill["value"]))
            list(self.loadPageOrder(skill["value"]))
            # results += list(self.loadPageOrder(skill["value"]))

    def loadPageOrder(self, skill=4209, page=1, totalcount=100, pageSize=100):
        dataurl = self.baseurl + "index.php?m=workorder&f=gridIndex"
        data = {"page": page, "rows": pageSize, "skillId": skill, "listType": "handle",
                "optid": "e7317288bb6d4849eec6dbe010d5d34e", "0[name]": "skill", "0[value]": skill,
                "1[name]": "Q|t2.dealstate|in", "1[value]": "OS_100,OS_400,OS_700,SS_W_REMIND",
                "27[name]": "isSearch", "27[value]": 1,
                "10[name]": "Q|t2.createtime|egt", "10[value]": BaseUtil.getDateBefore(3),
                "11[name]": "Q|t2.createtime|elt", "11[value]": BaseUtil.getDateBefore(0),
                }
        self.headers['Referer'] = dataurl
        print("loadPageOrder data ={}".format(data))
        response = self.session.post(dataurl, headers=self.headers, data=parse.urlencode(data))
        response.encoding = 'utf-8'
        print("loadOrders response={}".format(response.text))
        if response.status_code == 200:
            result = json.loads(response.text)
            totalcount = result['total']
            if page * pageSize >= totalcount:
                yield from self.parseOrders(result)
            else:
                yield from self.parseOrders(result)
                yield from self.loadPageOrder(page + 1, totalcount, pageSize)

    def parseOrders(self, data):
        for item in data['rows']:
            #         if ($temp['machinebrand'] == '峰米'){
            #         continue;
            #         }
            #         $temp['adminid'] =$adminid;
            #         $temp['factorynumber'] =$factorynumber;
            #         $db->insert('yxg_order_factory')->cols($temp)->query();
            yield {
                'factorynumber': item['worksn'], 'ordername': item['demandsmall'],
                'username': item['customername'], 'mobile': item['customertel'],
                'orderstatus': item['dealstate'], 'originname': item['srctype'],
                'machinetype': item['probcate_id'], 'machinebrand': item['brand_id'],
                # 'sn': '', 'version': item['PRODUCT_MODEL'] if 'PRODUCT_MODEL' in item else '',
                'repairtime': item['askdate'] + (" " + item['asktime']) if BaseUtil.is_timestr(item['asktime']) else '',
                'mastername': item['enginename'] if 'enginename' in item else '',
                'note': BeautifulSoup(item['processremark'], 'lxml').label.string,
                'companyid': self.factoryid, 'adminid': self.adminid,
                'address': BeautifulSoup(item['address'], 'lxml').label.string,
                # 'province': item['provinceName'], 'city': item['cityName'],
                # 'county': item['regionName'], 'town': item['countyName'],
                'ordertime': item['createtime'],
                'description': BeautifulSoup(item['clientrequirement'], 'lxml').label.string,
            }


if __name__ == '__main__':
    # util = ConkaUtil('K608475', 'Kuser6646!', adminid='20699', factoryid='1')
    util = TCSMUtil('AW3306009461', 'Md123456789!', adminid='24', factoryid='4')
    # util = ConkaUtil('K608069', 'Crm@20200401', adminid='24', factoryid='1')
    print(list(util.loadPageOrder()))
