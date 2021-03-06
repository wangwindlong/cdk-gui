import json

import requests
from bs4 import BeautifulSoup


class Util(object):
    @staticmethod
    def get_value(element):
        return element["value"]

    @staticmethod
    def get_selected(element):
        results = element.select('option[selected="selected"]')
        if results and len(results) > 0:
            return results[0]['value'] or ''
        option = element.find("option")
        if option:
            return option['value'] or ''
        return ''

    @staticmethod
    def getsoup(response):
        # print(response.status_code)
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, features="lxml")

    @staticmethod
    def finda(element):
        return element.find("a").text.strip()

    @staticmethod
    def findspan(element):
        return element.find("span").text.strip()

    @staticmethod
    def isNew(data, bjdomain, adminid):
        res = requests.post(bjdomain + "/Api/Climborder/checkexist",
                            data={"orderno": data['factorynumber'], 'adminid': adminid})
        return Util.checkBjRes(res)

    @staticmethod
    def getAccount(bjdomain):
        try:
            res = requests.post(bjdomain + "/Api/Climborder/newgetaccount", data={"mobile": "18205169014"})
            if res.status_code == 200 and res.text:
                result = json.loads(res.text)
                if 'ret' not in result or int(result['ret']) != 0 or 'element' not in result or not result['element']:
                    return None
                for factory in result['element']:
                    if 'factoryid' in factory and int(factory['factoryid']) == 10002 and len(factory['accounts']) > 0:
                        return factory['accounts'][0]
            else:
                return None
        except Exception as e:
            print("getaccount failed:", e)
            return None
        return None

    @staticmethod
    def clearKey(data, datakey, destkey='address'):
        if datakey in data and data[destkey] and data[destkey].strip().startswith(data[datakey].strip()):
            data[destkey] = data[destkey].replace(data[datakey], '', 1).strip()
        return data

    @staticmethod
    def clearAddress(orderinfo, destkey='address'):
        if destkey not in orderinfo:
            return orderinfo
        orderinfo = Util.clearKey(orderinfo, "province", destkey)
        orderinfo = Util.clearKey(orderinfo, "city", destkey)
        orderinfo = Util.clearKey(orderinfo, "county", destkey)
        orderinfo = Util.clearKey(orderinfo, "town", destkey)
        return orderinfo

    @staticmethod
    def checkBjRes(response):
        if response.status_code == 200 and response.text:
            result = json.loads(response.text)
            return 'ret' in result and int(result['ret']) == 0
        return False

    @staticmethod
    def getTableRow(bsObj, id, func, row_no=None, truncate=True):
        """@truncate: 是否截取掉最后一个字符"""
        table = bsObj.find("table", {"id": id})
        if not table:
            return ""
        alltr = table.find("tbody").find_all("tr")
        result = ""
        if row_no is not None and isinstance(row_no, int):
            if (0 <= row_no < len(alltr)) or (row_no < 0 and len(alltr) >= -row_no):
                return func(alltr[row_no].find_all("td")) if alltr[row_no] else ""
        for tr in alltr:
            note_td = tr.find_all("td")
            if note_td and len(note_td) > 2:
                item = func(note_td)
                result = result + item
        if truncate and result and len(result) > 0:
            result = result[:-1]
        return result
