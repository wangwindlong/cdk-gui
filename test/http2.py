import json

from hyper import HTTPConnection, HTTP20Connection

# conn = HTTPConnection('http2bin.org:443')
# conn.request('GET', '/get')
# resp = conn.get_response()
#
# print(resp.read())
from BaseUtil import BaseUtil

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
headers = {'Content-Type': 'application/x-www-form-urlencoded',
           'User-Agent': agent, 'Referer': "https://opn.jd.com/bill/search?billStatus=5",
           'Upgrade-Insecure-Requests': '1', 'Host': "opn.jd.com", 'Origin': "https://opn.jd.com",
           'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Accept': 'application/json, text/plain, */*'}

data = {"sort": "billId",
        "order": "desc",
        "billStatuses": "5",
        "isEgBuy": "0",
        "outletsNo": "05928613279",
        "sortKind": "4", "page": "1", "rows": "10", "isAppliance": "1",
        }
result = ""
for item in data:
    result += item + "=" + data[item] + "&"
result = result[:-1]
conn = HTTP20Connection(host='opn.jd.com', port=443)

cookie = BaseUtil.getCookie([{"domain": ".jd.com"}])
headers['Cookie'] = cookie
headers[':authority'] = 'opn.jd.com'
headers[':method'] = 'POST'
headers[':path'] = '/bill/query.json'
headers[':scheme'] = 'https'
response = conn.request(method='POST', url='https://opn.jd.com/bill/query.json',
                        body=result,
                        headers=headers)
resp = conn.get_response(response)
print(resp.status)
res = resp.read()
print(res)
print(json.loads(res))
