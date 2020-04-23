import requests
import httpx
import asyncio

response = requests.get("https://w.url.cn/s/AnYi1Bn", allow_redirects=False)
print(response.headers['location'])

response = requests.get("https://w.url.cn/s/AnYi1Bn")
print(response.url)

# from hyper.contrib import HTTP20Adapter
# s = requests.Session()
# s.mount('https://', HTTP20Adapter())
# r = s.get('https://cloudflare.com/')
# print(r.status_code)
# print(r.url)

r = httpx.get('https://www.example.org/')
print(r.text)
cookie = '__jdu=15822142358071336720677; shshshfpa=4cb610d9-d916-ed24-90ac-26170aa59905-1582214236; shshshfpb=dxacIi12p1xApuBdUnj4Zzw%3D%3D; TrackID=1b9lbGbVU7O61Fr6HyapmMEc5hjyhdzGpWAScmasqi25g6DrtqgeYZIPpPHABo56YVms-jaaKjHEIMGaIrAIofEENuJ91AbELXGk9pRasOq2yFaZraAqCYfmkDnUBBGPl; 3AB9D23F7A4B3C9B=JTSXKQXK7BUSY6MK36CKHJYFEZS6XKXYQJ56FG37H7VDCOLXLDJSLL4WZYQFXYPBSU2NQCGFFDSD3CAGULQAQ6GGNE; shshshfp=15280c7c63c160a1bb26518b39131b5e; __jdv=122270672|direct|-|none|-|1587581491593; cid=NXRPNDE2NnFJNTU0N2NTMzMwOGxENzcwMXBNNDc4MnVXMDE2M3FBOTUwNGdWOTMw; __jda=122270672.15822142358071336720677.1582214236.1587581492.1587614898.13; __jdc=122270672; wlfstk_smdl=o2abs2bgsy6d17syw26rvwab1ph7zbmn; thor=76167CD23714F158A010161AB3D4AD0189D6C181A37C49C8A0B98C6B2AD8D4DFAC4822D5E358CAEE26981F439B73624D72257F1274D0B17EC3F7FD6A75D1D0D6090111C7C7178673686607C91C11875FA1AA045AD69183B271C143EB33734E3D0A248D93D963BB2A74CB5AF19A5A3DB0D42C66710C2F8E466CD095F14F2129689CBE7FC484FCA7E7ECD62751F8CF0ED3; pinId=qPNJYlIyFdr3K3B-AGeThA; pin=djd0755860394; unick=jd_djd0486; ceshi3.com=000; _tp=aCXahsTQbNDTlwsCIhPtnQ%3D%3D; logining=1; _pst=djd0755860394; preAlpha=2.0.0'


def getCookies(cookie):
    try:
        s = cookie.split("; ")
        cookies = {}
        for c in s:
            content = c.split("=")
            if len(content) > 1:
                cookies[content[0]] = content[1]
        return cookies
    except Exception as e:
        print("getCookies", e)
        return ""


baseurl = 'https://jdfw.jd.com'
headers = {'content-type': 'application/x-www-form-urlencoded',
           'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
           'Upgrade-Insecure-Requests': '1', 'Host': 'jdfw.jd.com', 'Origin': baseurl,
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           "X-Requested-With": "XMLHttpRequest",
           'referer': 'https://jdfw.jd.com/receipt/receiptDashboardIndex?homePageDistinguish=notAppointed&serviceType=0',
           "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin"
           }

data = {
    "esSwitch": "1", "subCompanyId": "10", "wareInfoId": "lw_10_334%%603_2", "outletsId": "0755860394",
    "sortKind": "4", "page": "1", "rows": "20", "sort": "returnTime", "order": "desc", "serviceType": "0",
    "fastDealNum": "5"
}
result = ""
for item in data:
    result += item + "=" + data[item] + "&"
result = result + "freeinstall=&startStatus=&endStatus=&timeout=&todayOtherReservationConditionName=&productBrand=&productType1=&productType2=&productType3=&orderId=&bizOrderId=&ordernoGroup=&customerName=&customerPhone=&serviceStreet=&wareId=&productName=&orderStatus=&orderStatusGroup=&createOrderTimeBegin=&createOrderTimeEnd=&reservationDateBegin=&reservationDateEnd=&firstReservationTimeBegin=&firstReservationTimeEnd=&changedReservationDateBegin=&changedReservationDateEnd=&feedbackStatus=&orderOrderStatus=&expectAtHomeDateBegin=&expectAtHomeDateEnd=&atHomeFinishDateBegin=&atHomeFinishDateEnd=&deliveryDateStart=&deliveryDateEnd=&homePageDistinguish=&fastDealNumByColor=&reservationStatus=&reportLessFlag=&superExperienceStore=&sourceOrderIdGroup=&sellerId=&sellerName=&eclpBusinessNo=&isFast="


async def main(_baseurl, _data):
    async with httpx.AsyncClient(http2=True) as client:
        resp = await client.post(_baseurl + '/receipt/query.json',
                                 headers=headers, data=_data)
        print(resp.text)


asyncio.run(main(baseurl, result))
