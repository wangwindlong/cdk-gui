import codecs
import re
import time
from datetime import timedelta, date, datetime

import chardet

agents = [
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
]

# json1 = {"key1":"这个是1中的1", "key2":"这个是1中的2"}
# json2 = {"key1":"这个是2中的1", "key3":"这个是2中的3"}
# print(dict(json1, **json2))

# create_time = 1588123851000
# #转换成localtime
# time_local = time.localtime(create_time/1000)
# #转换成新的时间格式(2016-05-05 20:28:54)
# dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
# print(dt)

import json

text = '{"status":true,"content":false,"error":null}'
print(json.loads(text))
print((date.today() - timedelta(days=3)).strftime("%Y-%m-%d"))
print(round(time.time() * 1000))


def verify_date_str_lawyer(datetime_str):
    try:
        datetime.strptime(datetime_str, '%H:%M:%S')
        return True
    except ValueError:
        return False

print(verify_date_str_lawyer("12:20:20"))

# from bs4 import BeautifulSoup
# c1 = "<label title='福建省漳州市东山县西埔镇白石街顶巷550号'>福建省漳州市东山县西埔镇白石街顶巷550号<\/label>"
# # strinfo = re.compile('world')
# # d1 = strinfo.sub('python', c1)
# # print('1原始字符串:{}'.format(c1))
# # print('1替换字符串:{}'.format(d1))
# soup = BeautifulSoup(c1, 'lxml')
# print(soup.label.string)
#
# soup = BeautifulSoup('''<select name="skill" id="skill" class="technical">
# <option value="4209" selected="selected">C端业务</option>
# <option value="2226">彩电</option>
# <option value="1294">空调</option>
# <option value="1562">冰洗</option>
# </select>''', 'lxml')
# skills = soup.find("select", {"id": "skill"}).find_all("option")
# for skill in skills:
#     print(skill['value'])

# str = '志高（chigo）'
# print(re.sub(r'（[^（）]*）', '', str))
#
# str = '<label inte=fasdf> nihao<\/label>'
# print(re.sub(r'<label[^（）]*?>', '', str))

str = """﻿{"total":1,"rows":[{"id":"0c41fcb3a3d4dac40bb4334029a5a736","tid":"e7317288bb6d4849eec6dbe010d5d34e","skill_id":"4209","shop_id":"71e5fa032ced1e68a57731907ce3ca78","cpro_id":"8b05da6ccf50145d79118051a857c680","shopids":",71e5fa032ced1e68a57731907ce3ca78,","worksn":"WK200517132809015397","addresspath":"\/31\/482\/3204\/","customername":"\u738b","customertel":"18672555451\/18672555451","bigclass":"\u666e\u901a\u5ba2\u6237","proscate_id":"\u51c0\u6c34\u5668(\u5bb6\u7528RO\u673a)","caller":"18672555451","createtime":"2020-05-17 13:28:09","updatetime":"2020-05-20 15:21:45","transfertime":"0000-00-00 00:00:00","case_code":"<a href=\"javascript:void(0);\" onClick=popCaseInfo(\"98876abf2ad61b7fef6451ab1360a6b4\",\"51\",\"e7317288bb6d4849eec6dbe010d5d34e\")>CS2005171326014764<\/a>","case_id":"98876abf2ad61b7fef6451ab1360a6b4","engine_id":"889f8565db557ac85fd8e6cf5e5a714c","source_objid":"","dealstate":"\u5f85\u56de\u5355","dealsource":"\u6539\u7ea6","worktype":"0","sendnum":"1","istransferwork":"0","asktime":"\u65e0\u8981\u6c42","askdate":"2020-05-18","accepttime":"0000-00-00 00:00:00","departuretime":"0000-00-00 00:00:00","reachtime":"","finishtime":"0000-00-00 00:00:00","replytime":"0000-00-00 00:00:00","closetime":"0000-00-00 00:00:00","closereason":"","planstarttime":"2020-05-21 17:00:00","planendtime":"2020-05-21 17:00:00","changenum":"3","create_username":"TVFZFGS03","brand_id":"\u5341\u5206\u5230\u5bb6","probcate_id":"\u6c34\u5bb6\u7535","dembcate_id":"\u5b89\u8c03\u670d\u52a1","case_level":"\u666e\u901a\u5355","business_id":"\u670d\u52a1\u5355","phoneext":"51","sms_receipt":"<a class=\"J_showdialog\" data-id=\"add\" data-title=\"\u77ed\u4fe1\u91cd\u53d1\" data-uri=\"\/index.php?m=workorder&f=repeatSMS&engine_id=889f8565db557ac85fd8e6cf5e5a714c&workid=0c41fcb3a3d4dac40bb4334029a5a736\" onclick=\"javascript:repeatSMS(this);\" href=\"javascript:void(0);\">\u672a\u53d1\u9001<\/a>","extfield":"{\"amendtime\":\"2020-05-21 17:00:00\",\"remark\":\"\\u7528\\u6237\\u672a\\u63a5\\u7535\\u8bdd\\uff0c\\u6539\\u7ea622\\u53f7\",\"first_appoint_time\":\"2020-05-18 17:00:00\",\"last_amend_time\":\"2020-05-21 17:00:00\",\"last_amend_operation\":\"2020-05-20 15:21:45\"}","replysource":"EMT\uff08Android\uff09","isrepair":"0","shopname":"\u6f33\u5dde\u5e02\u8297\u57ce\u533a\u65b0\u4e2d\u7ef4\u5bb6\u7528\u7535\u5668\u7ef4\u4fee\u670d\u52a1\u90e8","enginename":"\u9648\u660e\u6bc5","buyshop":"","protype":"\u6b63\u54c1\u673a","srcorderno":"I396888013541121701","srctype":"\u5341\u5206\u5230\u5bb6","demandbig":"\u5b89\u8c03\u670d\u52a1","demandsmall":"\u8981\u6c42\u5b89\u8c03\u670d\u52a1","address":"<label title='\u798f\u5efa\u7701\u6f33\u5dde\u5e02\u4e1c\u5c71\u53bf\u897f\u57d4\u9547\u767d\u77f3\u8857\u9876\u5df7550\u53f7'>\u798f\u5efa\u7701\u6f33\u5dde\u5e02\u4e1c\u5c71\u53bf\u897f\u57d4\u9547\u767d\u77f3\u8857\u9876\u5df7550\u53f7<\/label>","clientrequirement":"<label title='\u5341\u5206\u5230\u5bb6,\u3010\u8ba2\u5355\u6765\u6e90\uff1a\u5fae\u4fe1\u7528\u6237\u6765\u6e90\u3011\u3010\u8ba2\u5355\u53f7:I396888013541121701\u3011\u3010\u4e00\u53e3\u4ef7\u5b89\u8c03\u670d\u52a1-\u5341\u5206\u5230\u5bb6-\u6c34\u5bb6\u7535-\u5b89\u8c03(\u4e0d\u542b\u8f85\u6750)\u3011\u3010\u5fae\u4fe1\u7528\u6237\u6765\u6e90\u3011\u6536\u53d6\u8d39\u7528120.00\u5143\uff0c\u9884\u7ea6\u65f6\u95f42020-5-18\u7684\u4e0a\u5348\u3002'>\u5341\u5206\u5230\u5bb6,\u3010\u8ba2\u5355\u6765\u6e90\uff1a\u5fae\u4fe1\u7528\u6237\u6765\u6e90\u3011\u3010\u8ba2\u5355\u53f7:I396888013541121701\u3011\u3010\u4e00\u53e3\u4ef7\u5b89\u8c03\u670d\u52a1-\u5341\u5206\u5230\u5bb6-\u6c34\u5bb6\u7535-\u5b89\u8c03(\u4e0d\u542b\u8f85\u6750)\u3011\u3010\u5fae\u4fe1\u7528\u6237\u6765\u6e90\u3011\u6536\u53d6\u8d39\u7528120.00\u5143\uff0c\u9884\u7ea6\u65f6\u95f42020-5-18\u7684\u4e0a\u5348\u3002<\/label>","contactnum":"1","bglevel":0,"durationtime":"94 \u5c0f\u65f611 \u5206","skillname":"C\u7aef\u4e1a\u52a1","amendtime":"2020-05-21 17:00:00","processremark":"<label title='\u7528\u6237\u672a\u63a5\u7535\u8bdd\uff0c\u6539\u7ea622\u53f7'>\u7528\u6237\u672a\u63a5\u7535\u8bdd\uff0c\u6539\u7ea622\u53f7<\/label>"}]}"""
str = re.sub(r'<label[^（）]*?>', '', str)
str = str.replace("<\\/label>", "")
# def clean_str(str):
#     asc2 = ('0x00','0x01','0x02','0x03','0x04','0x05','0x06','0x07','0x08','0x09','0x09','0x0a','0x0a','0x0b','0x0c','0x0d','0x0e','0x0f','0x10','0x11','0x12','0x13','0x14','0x15','0x16','0x17','0x18','0x19','0x1a','0x1b','0x1c','0x1d','0x1e','0x1f','0x20','0x7f')
#     for x in asc2:
#         str = str.replace(chr(int(x, 16)),'')
#     return str
print(chardet.detect(str))
str = str.encode('gbk').decode('utf-8')
data = json.loads(str)

print(str)



