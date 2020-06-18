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
