import requests

headers = {'Server': 'nginx', 'Date': 'Thu, 16 Apr 2020 02:50:39 GMT', 'Content-Type': 'text/html; charset=UTF-8',
           'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive',
           'Set-Cookie': 'pass_ua=web; Domain=account.xiaomi.com; Max-Age=2147483647; Path=/; HttpOnly; Expires=Tue, 04-May-2088 14:04:46 CST, deviceId=wb_55555a41-df75-4365-96ea-62a2594624ed; Domain=account.xiaomi.com; Max-Age=2147483647; Path=/; Expires=Tue, 04-May-2088 14:04:46 CST, pass_trace=/Z1GPqMzzdsvvJRZmownd/MiecWGaqSQ5i6YHAvHStc+uEmk98qI0AvdtPILcfHgSkt5gLCeakNC5f39m+4gdNNWu0f0S2oNZpVFOxVTlQnXq5UtQHgH3Unui3zzyM0c; Domain=account.xiaomi.com; Max-Age=2147483647; Path=/; Expires=Tue, 04-May-2088 14:04:46 CST, pass_ua=web; Domain=account.xiaomi.com; Max-Age=2147483647; Path=/; HttpOnly; Expires=Tue, 04-May-2088 14:04:46 CST, userId=EXPIRED; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, userId=EXPIRED; domain=account.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, userId=EXPIRED; domain=.account.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, userId=EXPIRED; domain=.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, userId=EXPIRED; domain=account.xiaomi.com; path=/pass/auth; expires=Thu, 01-Dec-1994 16:00:00 GMT, userId=EXPIRED; domain=.xiaomi.com; path=/pass/auth; expires=Thu, 01-Dec-1994 16:00:00 GMT, serviceToken=EXPIRED; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, serviceToken=EXPIRED; domain=.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, serviceToken=EXPIRED; domain=account.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, serviceToken=EXPIRED; path=/pass/auth; expires=Thu, 01-Dec-1994 16:00:00 GMT, serviceToken=EXPIRED; domain=account.xiaomi.com; path=/pass/auth; expires=Thu, 01-Dec-1994 16:00:00 GMT, serviceToken=EXPIRED; domain=.xiaomi.com; path=/pass/auth; expires=Thu, 01-Dec-1994 16:00:00 GMT, cUserId=EXPIRED; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, cUserId=EXPIRED; domain=.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, cUserId=EXPIRED; domain=account.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, cUserId=EXPIRED; domain=account.xiaomi.com; path=/pass/auth; expires=Thu, 01-Dec-1994 16:00:00 GMT, cUserId=EXPIRED; domain=.xiaomi.com; path=/pass/auth; expires=Thu, 01-Dec-1994 16:00:00 GMT, passToken=EXPIRED; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, passToken=EXPIRED; domain=account.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, passToken=EXPIRED; domain=account.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, passToken=EXPIRED; path=/; secure; expires=Thu, 01-Dec-1994 16:00:00 GMT, passToken=EXPIRED; domain=account.xiaomi.com; path=/; secure; expires=Thu, 01-Dec-1994 16:00:00 GMT, passToken=EXPIRED; domain=account.xiaomi.com; path=/; secure; expires=Thu, 01-Dec-1994 16:00:00 GMT, continue=EXPIRED; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, sns_type=EXPIRED; domain=.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, etao_qs=EXPIRED; domain=account.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, uLocale=zh_CN; domain=.xiaomi.com; path=/; expires=Fri, 01-May-2020 02:50:39 GMT, theme=EXPIRED; domain=account.xiaomi.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT, JSESSIONID=aaaGokQB_q56-eLo0m8fx; path=/',
           'X-Frame-Options': 'SAMEORIGIN', 'Expires': 'Thu, 01 Dec 1994 16:00:00 GMT',
           'Cache-Control': 'no-cache, no-cache, no-cache', 'Content-Encoding': 'gzip',
           'Strict-Transport-Security': 'max-age=600'}

import time

import datetime

print(time.time())
print(int(round(time.time() * 1000)))
print(datetime.datetime.now())

# session = requests.Session()
# response = session.get("https://www.google.com")
# print(response.text)

cookie1 = 'deviceId=wb_ce1900e2-d307-474e-9f70-82db01c44f77; _aegis_pp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1ODcyNzMxOTgsImV4dHJhIjoicGFzc3BvcnQiLCJleHAiOjE1ODczNjMxOTgsImlzcyI6Ik1JLUlORk9TRUMiLCJhdWQiOiJ4bXMuYmUueGlhb21pLmNvbSIsInN1YiI6IjIxNTQ5MjkyODciLCJpYXQiOjE1ODcyNzMxOTh9.KrCidc1m6Smdq7wRvWj7Z0oBVV4pwl64ELDVicC4kFg_xdC7GWoVaWMcVQNR_4LeaqTwsOW2s9IJKjykM6K5Rw; pass_ptd=1; JSESSIONID=adce8c2c-7f8c-479d-b8ec-ac4a00609496; JSESSIONID=aaay7VmhcGEiA884Gm8fx; JSESSIONID=aaaSAHPvukAptgmOB-qgx; cUserId=9WoKEQRB9fVUADppwgOb3okY2Gk; cUserId=9WoKEQRB9fVUADppwgOb3okY2Gk; pExpireTime=-1; passInfo=login-end; passToken=V1:dOO7XiXI5QXwNc27bD5Rt817jonwHoJYQDa+2chLL5QZ3ony8dKUbFcLbpvG+6NKLNkm8aX46aOniRc1qS0cl0EM1fCQSs17QtnFQ96vHrdMluCH+dx/nk9IDr65tlIHAYayPNIfRQ8TfGsFpxDhxTDHJwNex0XHmp5XvHWVxyL61qF3K/bBdj3zMg4jla/bu8D+3Y7zaxyMTA5ugDy4WqSzdkB5CGlxOTAzuPUYXCE7Gct4JE9soaFwfeNvxZxd4FGXPVz+APFZdwB9hTL6eEPouUU0SBPgWS0ktFcgK0M=; pass_trace=JL1DqClfSPQyrHaXuTiY5JRwGwscDpbpKlyczyigVnzidMJIn9dK4sTGdN1Tqp09PGRyug7viEcVM2ohg1UtDC2C+QCSeGoUOUXj0FLXxwo5YHSTZujNQHW1YTqfb//q; pass_ua=web; serviceToken=zYTZtT7xDWdZfFuCoP7yh5oC4xdarRI/3IPzTGP9/+AJMLQQ0dFwjWmg/JjbiBruLi3hmSzHwKnTu4SfFaosISch051VqcGoIIBSnR58c3o=; tick=6583215047390668854; uLocale=zh_CN; userId=2154929287; userId=2154929287; userName=181***829; xmsbe_slh=PIA8hFb80jA7HJgQ2/yC9KSy2O4=; Hm_lpvt_02f2b1424a5046f7ae2353645198ca13=1587276061; Hm_lvt_02f2b1424a5046f7ae2353645198ca13=1587273200,1587275482; lastsource=account.xiaomi.com; localtimezone=28800; msttime=https%253A%252F%252Fxms.be.xiaomi.com%252Fadmin%252Fpage!main.action; msttime1=https%253A%252F%252Fxms.be.xiaomi.com%252Fadmin%252Fpage!main.action; mstuid=1587273198567_1787; mstz=--%E6%9C%8D%E5%8A%A1%E5%8D%95%E6%9F%A5%E8%AF%A2%7C%7C342941440.2%7C%7Chttps%253A%252F%252Faccount.xiaomi.com%252Fpass%252Fservicelogin%253Fcallback%253Dhttp%25253a%25252f%25252fxms.be.xiaomi.com%25252fsts%25253ffollowup%25253dhttp%2525253a%2525252f%2525252fxms.be.xiaomi.com%2525252fadmin%2525252fpage%25252521main.action%252526sign%25253dqykzc%2525252brmxwf4am3yytkrlvympby%2525253d%257Csid%253Dxmsbe%7C; xm_vistor=1587273198567_1787_1587275481693-1587276060823; xst=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoxNTg3Mjc2MDYyLCJjdXRPcmdJZCI6IldEQ04wMjcwMiIsImV4cCI6MTU4NzI3Nzg2MiwibWlsaWFvIjoyMTU0OTI5Mjg3LCJvcmdJZCI6IldEQ04wMjcwMiJ9.HiK3kTbszOBwS2xDdTsc8NG_R1Uhq4u0Glfe6jbhWTo;'
# cookie2 = 'uLocale=zh_CN; _aegis_pp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1ODcyNzMxOTgsImV4dHJhIjoicGFzc3BvcnQiLCJleHAiOjE1ODczNjMxOTgsImlzcyI6Ik1JLUlORk9TRUMiLCJhdWQiOiJ4bXMuYmUueGlhb21pLmNvbSIsInN1YiI6IjIxNTQ5MjkyODciLCJpYXQiOjE1ODcyNzMxOTh9.KrCidc1m6Smdq7wRvWj7Z0oBVV4pwl64ELDVicC4kFg_xdC7GWoVaWMcVQNR_4LeaqTwsOW2s9IJKjykM6K5Rw; localtimezone=28800; mstuid=1587273198567_1787; JSESSIONID=aaaSAHPvukAptgmOB-qgx; cUserId=9WoKEQRB9fVUADppwgOb3okY2Gk; userName=181***829; serviceToken=zYTZtT7xDWdZfFuCoP7yh5oC4xdarRI/3IPzTGP9/+AJMLQQ0dFwjWmg/JjbiBruLi3hmSzHwKnTu4SfFaosISch051VqcGoIIBSnR58c3o=; userId=2154929287; xmsbe_slh=PIA8hFb80jA7HJgQ2/yC9KSy2O4=; JSESSIONID=adce8c2c-7f8c-479d-b8ec-ac4a00609496; xm_vistor=1587273198567_1787_1587275481693-1587275481693; Hm_lvt_02f2b1424a5046f7ae2353645198ca13=1587273200,1587275482; mstz=--%E6%9C%8D%E5%8A%A1%E5%8D%95%E6%9F%A5%E8%AF%A2%7C%7C342941440.1%7C%7C%7C; Hm_lpvt_02f2b1424a5046f7ae2353645198ca13=1587275494; xst=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoxNTg3Mjc1NDk2LCJjdXRPcmdJZCI6IldEQ04wMjcwMiIsImV4cCI6MTU4NzI3NzI5NiwibWlsaWFvIjoyMTU0OTI5Mjg3LCJvcmdJZCI6IldEQ04wMjcwMiJ9.cc2HNxWh_BA1EHH3SYaiOX2BPXPkAZWzatDpRLHnl7c'
cookie2 = 'uLocale=zh_CN; _aegis_pp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1ODcyNzMxOTgsImV4dHJhIjoicGFzc3BvcnQiLCJleHAiOjE1ODczNjMxOTgsImlzcyI6Ik1JLUlORk9TRUMiLCJhdWQiOiJ4bXMuYmUueGlhb21pLmNvbSIsInN1YiI6IjIxNTQ5MjkyODciLCJpYXQiOjE1ODcyNzMxOTh9.KrCidc1m6Smdq7wRvWj7Z0oBVV4pwl64ELDVicC4kFg_xdC7GWoVaWMcVQNR_4LeaqTwsOW2s9IJKjykM6K5Rw; localtimezone=28800; mstuid=1587273198567_1787; JSESSIONID=aaaSAHPvukAptgmOB-qgx; cUserId=9WoKEQRB9fVUADppwgOb3okY2Gk; userName=181***829; serviceToken=zYTZtT7xDWdZfFuCoP7yh5oC4xdarRI/3IPzTGP9/+AJMLQQ0dFwjWmg/JjbiBruLi3hmSzHwKnTu4SfFaosISch051VqcGoIIBSnR58c3o=; userId=2154929287; xmsbe_slh=PIA8hFb80jA7HJgQ2/yC9KSy2O4=; JSESSIONID=adce8c2c-7f8c-479d-b8ec-ac4a00609496; xm_vistor=1587273198567_1787_1587275481693-1587275481693; Hm_lvt_02f2b1424a5046f7ae2353645198ca13=1587273200,1587275482; mstz=--%E6%9C%8D%E5%8A%A1%E5%8D%95%E6%9F%A5%E8%AF%A2%7C%7C342941440.1%7C%7C%7C; Hm_lpvt_02f2b1424a5046f7ae2353645198ca13=1587275494; xst=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoxNTg3Mjc1NDk2LCJjdXRPcmdJZCI6IldEQ04wMjcwMiIsImV4cCI6MTU4NzI3NzI5NiwibWlsaWFvIjoyMTU0OTI5Mjg3LCJvcmdJZCI6IldEQ04wMjcwMiJ9.cc2HNxWh_BA1EHH3SYaiOX2BPXPkAZWzatDpRLHnl7c'
s1 = cookie1.split("; ")
s2 = cookie2.split("; ")
cookies1 = {}
cookies2 = {}
for c in s1:
    content = c.split("=")
    cookies1[content[0]] = content[1]
for c in s2:
    content = c.split("=")
    cookies2[content[0]] = content[1]

for item in cookies1:
    if not item in cookie2:
        print(item, cookies1[item])
# print(cookies)

ttt = {"result": {"srvInfos": [
    {"sId": "AS2004173605512", "type": "AZ", "typeDesc": "安装", "status": "ServiceEnd", "statusDesc": "业务完成",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "5191101869112973",
     "goodsIds": "23367", "goodsNames": "小米净水器600G", "imeis": "23367/00045572", "sns": "23367/00045572",
     "customerName": "刘先生", "customerTel": "18321774573", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站",
     "orgSubType": None, "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 2271879607,
     "acceptorName": "王振", "createTime": 1587099503000, "updateTime": 1587114357000, "closeTime": None,
     "createFrom": "CALL_CENTER", "createFromDesc": "客服中心", "receiveExpressNo": "", "sendExpressNo": None,
     "statId": None, "reserveId": None, "fieldNumber": None, "isReserve": None, "takeNumberTime": None,
     "callNumberTime": None, "reserveStatus": 0, "serviceNumber": None, "updatePerson": 2271879607,
     "longitude": "116.81395744837039", "latitude": "32.53429072331802", "specialType": None, "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "H10001", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004173901675", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "5200415444101492",
     "goodsIds": "23055", "goodsNames": "米家变频滚筒洗衣机1A 8kg", "imeis": "23055/00081404", "sns": "23055/00081404",
     "customerName": "李传菊", "customerTel": "18156067196", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站",
     "orgSubType": None, "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019,
     "acceptorName": "姚银银", "createTime": 1587107528000, "updateTime": 1587108971000, "closeTime": None,
     "createFrom": "ORDER_PHYSICAL", "createFromDesc": "订单实物", "receiveExpressNo": "", "sendExpressNo": None,
     "statId": None, "reserveId": None, "fieldNumber": None, "isReserve": None, "takeNumberTime": None,
     "callNumberTime": None, "reserveStatus": 0, "serviceNumber": None, "updatePerson": 935086019,
     "longitude": "116.87102618297833", "latitude": "32.18155550481355", "specialType": None, "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004173901429", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "5200414405600599",
     "goodsIds": "23945", "goodsNames": "米家变频滚筒洗衣机1S 8kg", "imeis": "23945/00072807", "sns": "23945/00072807",
     "customerName": "刘建莉", "customerTel": "15555159626", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站",
     "orgSubType": None, "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019,
     "acceptorName": "姚银银", "createTime": 1587107410000, "updateTime": 1587108731000, "closeTime": None,
     "createFrom": "ORDER_PHYSICAL", "createFromDesc": "订单实物", "receiveExpressNo": "", "sendExpressNo": None,
     "statId": None, "reserveId": None, "fieldNumber": None, "isReserve": None, "takeNumberTime": None,
     "callNumberTime": None, "reserveStatus": 0, "serviceNumber": None, "updatePerson": 935086019,
     "longitude": "116.86925859800601", "latitude": "32.06052146146598", "specialType": None, "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004173307027", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "5200414417102795",
     "goodsIds": "23057", "goodsNames": "Redmi全自动波轮洗衣机1A 8kg", "imeis": "23057/00263801", "sns": "23057/00263801",
     "customerName": "王贤刚", "customerTel": "17855286825", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站",
     "orgSubType": None, "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019,
     "acceptorName": "姚银银", "createTime": 1587088276000, "updateTime": 1587089021000, "closeTime": None,
     "createFrom": "ORDER_PHYSICAL", "createFromDesc": "订单实物", "receiveExpressNo": "", "sendExpressNo": None,
     "statId": None, "reserveId": None, "fieldNumber": None, "isReserve": None, "takeNumberTime": None,
     "callNumberTime": None, "reserveStatus": 0, "serviceNumber": None, "updatePerson": 935086019,
     "longitude": "116.7171426510834", "latitude": "31.948818779309132", "specialType": None, "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "APPLY_CANCEL_1",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004173300611", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "0", "goodsIds": "25308",
     "goodsNames": "米家变频滚筒洗衣机1C 10kg", "imeis": None, "sns": "", "customerName": "先生", "customerTel": "17677418450",
     "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "orgSubType": None, "acceptOrgId": "WDCN02702",
     "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019, "acceptorName": "姚银银",
     "createTime": 1587085540000, "updateTime": 1587088700000, "closeTime": None, "createFrom": "CALL_CENTER",
     "createFromDesc": "客服中心", "receiveExpressNo": "", "sendExpressNo": None, "statId": None, "reserveId": None,
     "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None, "reserveStatus": 0,
     "serviceNumber": None, "updatePerson": 935086019, "longitude": "116.87763944705802",
     "latitude": "32.36778602165519", "specialType": None, "omsServiceType": None, "omsServiceTypeDesc": None,
     "createOrgId": "H10001", "businessType": None, "businessSubType": None, "businessTypeDesc": None,
     "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE", "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004164201017", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "1200317440811412",
     "goodsIds": "17086", "goodsNames": "小米净水器1A（厨下式）白色", "imeis": "17086/20105459", "sns": "17086/20105459",
     "customerName": "张李莉", "customerTel": "13671647869", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站",
     "orgSubType": None, "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 2194224313,
     "acceptorName": "周鑫", "createTime": 1587031738000, "updateTime": 1587088478000, "closeTime": None,
     "createFrom": "MI_COM", "createFromDesc": "小米官网", "receiveExpressNo": "", "sendExpressNo": None, "statId": None,
     "reserveId": None, "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None,
     "reserveStatus": 0, "serviceNumber": None, "updatePerson": 2194224313, "longitude": "116.71427950079587",
     "latitude": "32.16549660929186", "specialType": None, "omsServiceType": None, "omsServiceTypeDesc": None,
     "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None, "businessTypeDesc": None,
     "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE", "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004164205580", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "1200416472202647",
     "goodsIds": "19927", "goodsNames": "空调(室内机)(1.5匹/变频/三级能效)", "imeis": "", "sns": "", "customerName": "王锦文",
     "customerTel": "13739231377", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "orgSubType": None,
     "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019, "acceptorName": "姚银银",
     "createTime": 1587034323000, "updateTime": 1587084462000, "closeTime": None, "createFrom": "TMALL_SEND_INSTALL",
     "createFromDesc": "天猫安装服务", "receiveExpressNo": "", "sendExpressNo": None, "statId": None, "reserveId": None,
     "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None, "reserveStatus": 0,
     "serviceNumber": None, "updatePerson": 935086019, "longitude": "116.90867674683493",
     "latitude": "32.06905126739108", "specialType": "XMS_AIR_CONDITIONING", "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004164205580", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "1200416472202647",
     "goodsIds": "19928", "goodsNames": "空调(室外机)(1.5匹/变频/三级能效)", "imeis": "", "sns": "", "customerName": "王锦文",
     "customerTel": "13739231377", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "orgSubType": None,
     "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019, "acceptorName": "姚银银",
     "createTime": 1587034323000, "updateTime": 1587084462000, "closeTime": None, "createFrom": "TMALL_SEND_INSTALL",
     "createFromDesc": "天猫安装服务", "receiveExpressNo": "", "sendExpressNo": None, "statId": None, "reserveId": None,
     "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None, "reserveStatus": 0,
     "serviceNumber": None, "updatePerson": 935086019, "longitude": "116.90867674683493",
     "latitude": "32.06905126739108", "specialType": "XMS_AIR_CONDITIONING", "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004164205576", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "1200416472202647",
     "goodsIds": "19927", "goodsNames": "空调(室内机)(1.5匹/变频/三级能效)", "imeis": "", "sns": "", "customerName": "王锦文",
     "customerTel": "13739231377", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "orgSubType": None,
     "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019, "acceptorName": "姚银银",
     "createTime": 1587034323000, "updateTime": 1587084436000, "closeTime": None, "createFrom": "TMALL_SEND_INSTALL",
     "createFromDesc": "天猫安装服务", "receiveExpressNo": "", "sendExpressNo": None, "statId": None, "reserveId": None,
     "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None, "reserveStatus": 0,
     "serviceNumber": None, "updatePerson": 935086019, "longitude": "116.90867674683493",
     "latitude": "32.06905126739108", "specialType": "XMS_AIR_CONDITIONING", "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004164205576", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "1200416472202647",
     "goodsIds": "19928", "goodsNames": "空调(室外机)(1.5匹/变频/三级能效)", "imeis": "", "sns": "", "customerName": "王锦文",
     "customerTel": "13739231377", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "orgSubType": None,
     "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019, "acceptorName": "姚银银",
     "createTime": 1587034323000, "updateTime": 1587084436000, "closeTime": None, "createFrom": "TMALL_SEND_INSTALL",
     "createFromDesc": "天猫安装服务", "receiveExpressNo": "", "sendExpressNo": None, "statId": None, "reserveId": None,
     "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None, "reserveStatus": 0,
     "serviceNumber": None, "updatePerson": 935086019, "longitude": "116.90867674683493",
     "latitude": "32.06905126739108", "specialType": "XMS_AIR_CONDITIONING", "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None}], "pageInfo": {"total": 30, "list": [
    {"sId": "AS2004173605512", "type": "AZ", "typeDesc": "安装", "status": "ServiceEnd", "statusDesc": "业务完成",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "5191101869112973",
     "goodsIds": "23367", "goodsNames": "小米净水器600G", "imeis": "23367/00045572", "sns": "23367/00045572",
     "customerName": "刘先生", "customerTel": "18321774573", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站",
     "orgSubType": None, "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 2271879607,
     "acceptorName": "王振", "createTime": 1587099503000, "updateTime": 1587114357000, "closeTime": None,
     "createFrom": "CALL_CENTER", "createFromDesc": "客服中心", "receiveExpressNo": "", "sendExpressNo": None,
     "statId": None, "reserveId": None, "fieldNumber": None, "isReserve": None, "takeNumberTime": None,
     "callNumberTime": None, "reserveStatus": 0, "serviceNumber": None, "updatePerson": 2271879607,
     "longitude": "116.81395744837039", "latitude": "32.53429072331802", "specialType": None, "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "H10001", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004173901675", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "5200415444101492",
     "goodsIds": "23055", "goodsNames": "米家变频滚筒洗衣机1A 8kg", "imeis": "23055/00081404", "sns": "23055/00081404",
     "customerName": "李传菊", "customerTel": "18156067196", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站",
     "orgSubType": None, "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019,
     "acceptorName": "姚银银", "createTime": 1587107528000, "updateTime": 1587108971000, "closeTime": None,
     "createFrom": "ORDER_PHYSICAL", "createFromDesc": "订单实物", "receiveExpressNo": "", "sendExpressNo": None,
     "statId": None, "reserveId": None, "fieldNumber": None, "isReserve": None, "takeNumberTime": None,
     "callNumberTime": None, "reserveStatus": 0, "serviceNumber": None, "updatePerson": 935086019,
     "longitude": "116.87102618297833", "latitude": "32.18155550481355", "specialType": None, "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004173901429", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "5200414405600599",
     "goodsIds": "23945", "goodsNames": "米家变频滚筒洗衣机1S 8kg", "imeis": "23945/00072807", "sns": "23945/00072807",
     "customerName": "刘建莉", "customerTel": "15555159626", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站",
     "orgSubType": None, "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019,
     "acceptorName": "姚银银", "createTime": 1587107410000, "updateTime": 1587108731000, "closeTime": None,
     "createFrom": "ORDER_PHYSICAL", "createFromDesc": "订单实物", "receiveExpressNo": "", "sendExpressNo": None,
     "statId": None, "reserveId": None, "fieldNumber": None, "isReserve": None, "takeNumberTime": None,
     "callNumberTime": None, "reserveStatus": 0, "serviceNumber": None, "updatePerson": 935086019,
     "longitude": "116.86925859800601", "latitude": "32.06052146146598", "specialType": None, "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004173307027", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "5200414417102795",
     "goodsIds": "23057", "goodsNames": "Redmi全自动波轮洗衣机1A 8kg", "imeis": "23057/00263801", "sns": "23057/00263801",
     "customerName": "王贤刚", "customerTel": "17855286825", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站",
     "orgSubType": None, "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019,
     "acceptorName": "姚银银", "createTime": 1587088276000, "updateTime": 1587089021000, "closeTime": None,
     "createFrom": "ORDER_PHYSICAL", "createFromDesc": "订单实物", "receiveExpressNo": "", "sendExpressNo": None,
     "statId": None, "reserveId": None, "fieldNumber": None, "isReserve": None, "takeNumberTime": None,
     "callNumberTime": None, "reserveStatus": 0, "serviceNumber": None, "updatePerson": 935086019,
     "longitude": "116.7171426510834", "latitude": "31.948818779309132", "specialType": None, "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "APPLY_CANCEL_1",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004173300611", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "0", "goodsIds": "25308",
     "goodsNames": "米家变频滚筒洗衣机1C 10kg", "imeis": None, "sns": "", "customerName": "先生", "customerTel": "17677418450",
     "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "orgSubType": None, "acceptOrgId": "WDCN02702",
     "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019, "acceptorName": "姚银银",
     "createTime": 1587085540000, "updateTime": 1587088700000, "closeTime": None, "createFrom": "CALL_CENTER",
     "createFromDesc": "客服中心", "receiveExpressNo": "", "sendExpressNo": None, "statId": None, "reserveId": None,
     "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None, "reserveStatus": 0,
     "serviceNumber": None, "updatePerson": 935086019, "longitude": "116.87763944705802",
     "latitude": "32.36778602165519", "specialType": None, "omsServiceType": None, "omsServiceTypeDesc": None,
     "createOrgId": "H10001", "businessType": None, "businessSubType": None, "businessTypeDesc": None,
     "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE", "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004164201017", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "1200317440811412",
     "goodsIds": "17086", "goodsNames": "小米净水器1A（厨下式）白色", "imeis": "17086/20105459", "sns": "17086/20105459",
     "customerName": "张李莉", "customerTel": "13671647869", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站",
     "orgSubType": None, "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 2194224313,
     "acceptorName": "周鑫", "createTime": 1587031738000, "updateTime": 1587088478000, "closeTime": None,
     "createFrom": "MI_COM", "createFromDesc": "小米官网", "receiveExpressNo": "", "sendExpressNo": None, "statId": None,
     "reserveId": None, "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None,
     "reserveStatus": 0, "serviceNumber": None, "updatePerson": 2194224313, "longitude": "116.71427950079587",
     "latitude": "32.16549660929186", "specialType": None, "omsServiceType": None, "omsServiceTypeDesc": None,
     "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None, "businessTypeDesc": None,
     "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE", "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004164205580", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "1200416472202647",
     "goodsIds": "19927", "goodsNames": "空调(室内机)(1.5匹/变频/三级能效)", "imeis": "", "sns": "", "customerName": "王锦文",
     "customerTel": "13739231377", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "orgSubType": None,
     "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019, "acceptorName": "姚银银",
     "createTime": 1587034323000, "updateTime": 1587084462000, "closeTime": None, "createFrom": "TMALL_SEND_INSTALL",
     "createFromDesc": "天猫安装服务", "receiveExpressNo": "", "sendExpressNo": None, "statId": None, "reserveId": None,
     "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None, "reserveStatus": 0,
     "serviceNumber": None, "updatePerson": 935086019, "longitude": "116.90867674683493",
     "latitude": "32.06905126739108", "specialType": "XMS_AIR_CONDITIONING", "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004164205580", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "1200416472202647",
     "goodsIds": "19928", "goodsNames": "空调(室外机)(1.5匹/变频/三级能效)", "imeis": "", "sns": "", "customerName": "王锦文",
     "customerTel": "13739231377", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "orgSubType": None,
     "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019, "acceptorName": "姚银银",
     "createTime": 1587034323000, "updateTime": 1587084462000, "closeTime": None, "createFrom": "TMALL_SEND_INSTALL",
     "createFromDesc": "天猫安装服务", "receiveExpressNo": "", "sendExpressNo": None, "statId": None, "reserveId": None,
     "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None, "reserveStatus": 0,
     "serviceNumber": None, "updatePerson": 935086019, "longitude": "116.90867674683493",
     "latitude": "32.06905126739108", "specialType": "XMS_AIR_CONDITIONING", "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004164205576", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "1200416472202647",
     "goodsIds": "19927", "goodsNames": "空调(室内机)(1.5匹/变频/三级能效)", "imeis": "", "sns": "", "customerName": "王锦文",
     "customerTel": "13739231377", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "orgSubType": None,
     "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019, "acceptorName": "姚银银",
     "createTime": 1587034323000, "updateTime": 1587084436000, "closeTime": None, "createFrom": "TMALL_SEND_INSTALL",
     "createFromDesc": "天猫安装服务", "receiveExpressNo": "", "sendExpressNo": None, "statId": None, "reserveId": None,
     "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None, "reserveStatus": 0,
     "serviceNumber": None, "updatePerson": 935086019, "longitude": "116.90867674683493",
     "latitude": "32.06905126739108", "specialType": "XMS_AIR_CONDITIONING", "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None},
    {"sId": "AS2004164205576", "type": "AZ", "typeDesc": "安装", "status": "ReadyDepart", "statusDesc": "待出发",
     "serviceWay": "DJ", "wayDesc": "到家", "subWay": "DJ_MF", "subWayDesc": "免费到家", "orderIds": "1200416472202647",
     "goodsIds": "19928", "goodsNames": "空调(室外机)(1.5匹/变频/三级能效)", "imeis": "", "sns": "", "customerName": "王锦文",
     "customerTel": "13739231377", "orgId": "WDCN02702", "orgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "orgSubType": None,
     "acceptOrgId": "WDCN02702", "acceptOrgName": "合肥佳元子站-淮南佳元-寿县佳元上门综合站", "acceptor": 935086019, "acceptorName": "姚银银",
     "createTime": 1587034323000, "updateTime": 1587084436000, "closeTime": None, "createFrom": "TMALL_SEND_INSTALL",
     "createFromDesc": "天猫安装服务", "receiveExpressNo": "", "sendExpressNo": None, "statId": None, "reserveId": None,
     "fieldNumber": None, "isReserve": None, "takeNumberTime": None, "callNumberTime": None, "reserveStatus": 0,
     "serviceNumber": None, "updatePerson": 935086019, "longitude": "116.90867674683493",
     "latitude": "32.06905126739108", "specialType": "XMS_AIR_CONDITIONING", "omsServiceType": None,
     "omsServiceTypeDesc": None, "createOrgId": "WDCN02702", "businessType": None, "businessSubType": None,
     "businessTypeDesc": None, "businessSubTypeDesc": None, "windowNo": None, "cancelFlag": "NONE",
     "rejectCancelTimes": 0, "goodsCode": None}], "pageNum": 1, "pageSize": 10, "size": 10, "startRow": 1, "endRow": 10,
                                                               "pages": 3, "prePage": 0, "nextPage": 2,
                                                               "isFirstPage": 1, "isLastPage": 0,
                                                               "hasPreviousPage": 0, "hasNextPage": 1,
                                                               "navigatePages": 8, "navigatepageNums": [1, 2, 3],
                                                               "navigateFirstPage": 1, "navigateLastPage": 3},
    "limitClose": 1}, "code": 1, "message": "ok"}

# print("=======ttt")
# print(len(ttt['result']['srvInfos']))
# print(len(ttt['result']['pageInfo']['list']))
#
#
# def test():
#     return []
#
#
# print(list(test()))
