import json
import time
from datetime import date, timedelta

import requests

from BaseUtil import BaseUtil
from cookie_test import fetch_chrome_cookie


class MideaUtil(BaseUtil):

    def __init__(self, username, passwd, adminid='24', factoryid='4', baseurl='https://cs.midea.com/c-css/',
                 bjdomain='http://yxgtest.bangjia.me'):
        super(MideaUtil, self).__init__(username, passwd, adminid, factoryid, baseurl, bjdomain)
        self.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng," \
                                 "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        self.dataverify = {'code': 2, 'msg': '输入验证码', 'element': ''}
        self.cookie = fetch_chrome_cookie([{"domain": ".midea.com"}], isExact=False)
        # self.cookie = 'JSESSIONID=918ED2F00EF0EC320CDC8A7D23C5393E; encryptPas=2b6a30073a6c0367f2a365f45b638afcbda90aeb3b03ed64214cbe2a4ac843393b5306d68dad41f81b2bf5d7b228c36baa55145dafefc88edf520c4874e159e2; rxVisitor=1589504557416CGLO4ELDDDQDDJ4G0ML7KGDK2I5D6VEE; loginToken=AW33060094617a9c6e2848a04d908b44d14411a11493; account=AW3306009461; menuVersionS=NEW; skinColor=%230092d7; loginEntity=CS006; isRefresh=true; lastIndex=0; midea_sso_token=Iv3S%2BQn5Uj79UBwWmw7DZksPe5C2%2BJlAmC1CenZXzrtu14nxwYeeUB%2BRC1ihJ2T7; MAS_TGC=eyJhbGciOiJIUzUxMiJ9.WlhsS05tRllRV2xQYVVwRlVsVlphVXhEU21oaVIyTnBUMmxLYTJGWVNXbE1RMHBzWW0xTmFVOXBTa0pOVkVrMFVUQktSRXhWYUZSTmFsVXlTVzR3TGk1b2JuSmZXV2hUYkVGRVdXcGFjMmhwTldaVlVXSkJMbFZoZUZCNU5YVmxSbk5YWWpSS2JWSmFhbFpWYmxSMWNWUTVjWFp5V0VGVlNrSldNamRpTkRsNFZqaGhWemQ1WkZGc1RYazFWbFJYVkhJM1pXdDBWa3RXTjJwaU5sOXRURXAxVkd4VFNUY3hlVTVUVVVWQldVMTRWSGhHYTNaTFNVRjNiVGxxT0RGbk9FRnliakJhYTJJd2NFNUhOazFGY1U5WGIzQlZRMjl0UW5aRVVHeG1kRlF4VTNWR01EVkNPRkIzTmpSSVNteHNiMnhDV1dKQmFrbHBWR2t4TkRKamRXOUJkeTVpUm05M1ZHRmliRkZZYTJOdFNHUm9WSFV6YnpGQg.FCuKkht0dC7aw0ZskROn_g4QWtd9RBgtq_krnETgig2wx3Q8yq7L8ABDYNWnbwQtWw1H06Wwxp3QLp9n8zJEgA; trackSwitch=Y; dtCookie=19$3E79717D3FB126610E30E06B5355209A|0d17e778a2d1917d|0; dtSa=-; dtLatC=10; rxvt=1589507463669|1589504557420; dtPC=19$105576887_337h31p19$105659306_993h46vCIPACBDJGJOAKHDJJIDEIFBOELEAKJMJ'
        self.cookies = BaseUtil.getCookies(self.cookie)
        self.headers['Cookie'] = self.cookie

    def loadOrders(self, param=None):
        try:
            data = {"data": json.dumps(list(self.loadPageOrder()))}
            requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
        except:
            return self.datafail
        return self.datasuccess

    def loadPageOrder(self, page=1, totalcount=100, pageSize=100):
        # 开始加载工单
        self.headers['Accept'] = "*/*"
        self.headers['Content-Type'] = 'application/json'
        dataurl = self.baseurl + "womflow/serviceorderunit/listdata"
        data = {"page": page, "rows": pageSize, "pageIndex": page - 1, "pageSize": pageSize,
                "formConditions": {"SERVICE_ORDER_STATUS": "",
                                   "CONTACT_TIME": (date.today() - timedelta(days=7)).strftime("%Y-%m-%d"),
                                   "CONTACT_TIME_end": (date.today()).strftime("%Y-%m-%d")}}
        response = self.session.post(dataurl, headers=self.headers, data=json.dumps(data))
        self.headers['Referer'] = self.baseurl + "womflow/serviceorderunit/list?type=womServiceNotFinshCount"
        response.encoding = 'utf-8'
        print("loadOrders response={}".format(response.text))
        result = json.loads(response.text)
        if result and 'status' in result and result['status']:
            data = result['content']
            totalcount = data['total']
            pagecount = data['pageCount']
            pageSize = data['pageSize']
            page = data['pageIndex']
            print("totalcount={} pagecount={} pageSize={} page={}".format(totalcount, pagecount, pageSize, page))
            if page >= pagecount:
                yield from self.parseOrders(data)
            else:
                yield from self.parseOrders(data)
                yield from self.loadPageOrder(page + 1, totalcount, pageSize)

    def parseOrders(self, data):
        for item in data['rows']:
            yield {
                'factorynumber': item['SERVICE_ORDER_NO'], 'ordername': item['SERVICE_SUB_TYPE_NAME'],
                'username': item['SERVICE_CUSTOMER_NAME'], 'mobile': item['SERVICE_CUSTOMER_TEL1'],
                'orderstatus': item['SERVICE_ORDER_STATUS'], 'originname': item['ORDER_ORIGIN'],
                'machinetype': item['PROD_NAME'], 'machinebrand': item['BRAND_NAME'],
                'sn': '', 'version': item['PRODUCT_MODEL'] if 'PRODUCT_MODEL' in item else '',
                'repairtime': item['FINAL_APPOINT_TIME'] if 'FINAL_APPOINT_TIME' in item else '',
                'mastername': item['ENGINEER_NAME'] if 'ENGINEER_NAME' in item else '',
                'note': item['PUB_REMARK'] if 'PUB_REMARK' in item else '',
                'companyid': self.factoryid, 'adminid': self.adminid,
                'address': str(item['SERVICE_CUSTOMER_ADDRESS']),
                # 'province': item['provinceName'], 'city': item['cityName'],
                # 'county': item['regionName'], 'town': item['countyName'],
                'ordertime': item['CONTACT_TIME'],
                'description': item['SERVICE_DESC'],
            }


if __name__ == '__main__':
    # util = ConkaUtil('K608475', 'Kuser6646!', adminid='20699', factoryid='1')
    util = MideaUtil('AW3306009461', 'Md123456789!', adminid='24', factoryid='4')
    # util = ConkaUtil('K608069', 'Crm@20200401', adminid='24', factoryid='1')
    print(util.loadOrders())
