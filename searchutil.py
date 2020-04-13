import json

import requests

base_url = "http://114.55.168.6/"
search_api = base_url + "es-test/essearch.php"
oper_api = base_url + "es-test/oper-search.php"


# 操作类别：1:建单 2:派单 3:审核 4:结算 5:回访
def getAdminids():
    params = dict()
    params['method'] = 'search'
    params['index'] = 'yxgoper'
    params['from'] = 0
    params['size'] = 30
    params['groupby'] = 'adminid'
    params['keyword'] = ''
    params['field_return'] = 'adminid'
    checkRes = requests.post(search_api, data=params)
    checkRes.encoding = 'utf-8'

    adminids = []
    if checkRes and checkRes.status_code == 200:
        # print("获取所有网点id成功：")
        # print(checkRes.text)
        results = json.loads(checkRes.text)
        adminids.append('24')
        for element in results['element']:
            adminids.append(str(element['adminid']))
    return adminids


def getMasters(adminid):
    params = dict()
    params['method'] = 'search'
    params['index'] = 'yxgoper'
    params['from'] = 0
    params['size'] = 100
    params['groupby'] = 'username'
    params['keyword'] = ''
    params['field_return'] = ['username', 'userid']
    params['adminid'] = adminid
    checkRes = requests.post(search_api, data=params)
    checkRes.encoding = 'utf-8'

    adminids = []
    if checkRes and checkRes.status_code == 200:
        # print("获取所有网点id成功：")
        print(checkRes.text)
        results = json.loads(checkRes.text)
        adminids.append({'userid': '', 'username': '全部'})
        for element in results['element']:
            adminids.append(element)
    return adminids


# print(getMasters(24))

def getOperators(adminid, userid, start, end):
    params = dict()
    params['method'] = 'search'
    params['index'] = 'yxgoper'
    params['from'] = 0
    params['size'] = 100
    params['groupby'] = 'opertype'
    params['keyword'] = ''
    params['opertime'] = json.dumps([['egt', start], ['elt', end], 'and'])
    params['userids'] = json.dumps(userid)
    params['field_return'] = json.dumps(['username', 'opertype'])
    params['adminid'] = adminid
    checkRes = requests.post(oper_api, data=params)
    checkRes.encoding = 'utf-8'

    opers = []
    if checkRes and checkRes.status_code == 200:
        # print("获取所有网点id成功：")
        print(checkRes.text)
        results = json.loads(checkRes.text)
        for element in results['element']:
            opers.append(element)
    return opers

# print(getMasters('24'))
# print(getOperators('24', ['250', '281', '23'], '2020-01-08 00:00:00', '2020-05-08 00:00:00'))
