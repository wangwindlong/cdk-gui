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
    def checkBjRes(response):
        if response.status_code == 200 and response.text:
            result = json.loads(response.text)
            return 'ret' in result and int(result['ret']) == 0
        return False
