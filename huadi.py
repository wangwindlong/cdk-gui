import json
import math
import re
import time
import urllib.parse
from io import BytesIO
import pycurl
from bs4 import BeautifulSoup
# from graborder.logbook import add_api_log

out_time = 30
def login_hd(url, username, pwd):
    try:
        ch = pycurl.Curl()
        buffer_con = BytesIO()
        ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
        ch.setopt(pycurl.URL, url + "/irj/portal")
        ch.setopt(pycurl.HEADER, 1)
        ch.setopt(pycurl.USERAGENT,
                  "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 "
                  "Safari/537.36")
        ch.setopt(pycurl.TIMEOUT, out_time)
        ch.perform()
        htmlelement = buffer_con.getvalue()
        buffer_con.close()
        ch.close()
        htmlelement = str(htmlelement, encoding="utf-8")
        cookies = re.findall(r'set-cookie:(.*)', htmlelement)
        jsessionid = ''
        i = 0
        while i < len(cookies):
            jsessionid += cookies[i].strip() + ";"
            i = i + 1
        loginpage = BeautifulSoup(htmlelement, "html.parser")
        inputobj = loginpage.select('input')
        j_salt = inputobj[3].get('value')
        login_data = "login_do_redirect=1&no_cert_storing=on&login_submit=on&j_salt=" + j_salt + "&j_username=" + username + "&j_password=" + pwd + "&uidPasswordLogon='登录'"
        login_data = login_data.encode("utf-8")
        c = pycurl.Curl()
        buffer_con1 = BytesIO()
        c.setopt(pycurl.URL, url + "/irj/portal")
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, login_data)
        c.setopt(pycurl.USERAGENT,
                 "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110"
                 "Safari/537.36")
        c.setopt(pycurl.COOKIE, jsessionid)
        c.setopt(pycurl.WRITEFUNCTION, buffer_con1.write)
        c.setopt(pycurl.TIMEOUT, out_time)
        c.perform()
        res = buffer_con1.getvalue()
        buffer_con1.close()
        c.close()
        res = str(res, encoding="utf-8")
        if res.find('Go to the temporary') != -1:
            ch1 = pycurl.Curl()
            buffer_con2 = BytesIO()
            ch1.setopt(pycurl.URL, url + "/irj/portal")
            ch1.setopt(pycurl.POST, 1)
            ch1.setopt(pycurl.POSTFIELDS, login_data)
            ch1.setopt(pycurl.HEADER, 1)
            ch1.setopt(pycurl.USERAGENT,
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 "
                       "Safari/537.36")
            ch1.setopt(pycurl.COOKIE, jsessionid)
            ch1.setopt(pycurl.WRITEFUNCTION, buffer_con2.write)
            ch1.setopt(pycurl.TIMEOUT, out_time)
            ch1.perform()
            res1 = buffer_con2.getvalue()
            buffer_con2.close()
            ch1.close()
            res1 = str(res1, encoding="utf-8")
            cookies2 = re.findall(r'set-cookie:(.*)', res1)
            j = 0
            while j < len(cookies2):
                jsessionid += cookies2[j].strip() + ";"
                j = j + 1
            return {'code': 1, 'msg': '', 'element': jsessionid}
        else:
            return {'code': 0, 'msg': '登录失败'}
    except Exception as e:
        return {'code': 0, 'msg': str(e)}


def url_encoder(params):
    g_encode_params = {}

    def _encode_params(params, p_key=None):
        encode_params = {}
        if isinstance(params, dict):
            for k in params:
                encode_key = '{}[{}]'.format(p_key, k)
                encode_params[encode_key] = params[k]
        elif isinstance(params, (list, tuple)):
            for offset, value in enumerate(params):
                encode_key = '{}[{}]'.format(p_key, offset)
                encode_params[encode_key] = value
        else:
            g_encode_params[p_key] = params

        for k in encode_params:
            value = encode_params[k]
            _encode_params(value, k)

    if isinstance(params, dict):
        for k in params:
            _encode_params(params[k], k)
    return urllib.parse.urlencode(g_encode_params)


def get_jid(cookie):
    j_id = re.findall("JSESSIONID=(.*)", cookie)
    j_id1 = j_id[0].split(";")
    return j_id1[0][0:40]


def get_orders(orderdata_dom, url, cookie, strkey, admin_id, bjdomain,mobile):
    try:
        k1 = 0
        order_list = {}
        print("hd--> get_orders  start >>> ")
        for input_obj in orderdata_dom.select(".urLnkFunction"):
            ordername = input_obj.find_parent().find_next_sibling().get_text()
            if ordername[0:2] not in ['安装', '维修', '增值']:
                continue

            ch7 = pycurl.Curl()
            buffer_con7 = BytesIO()
            ch7.setopt(ch7.WRITEFUNCTION, buffer_con7.write)
            ch7.setopt(ch7.URL, bjdomain + "/Api/Climborder/checkexist")
            ch7.setopt(ch7.POST, 1)
            ch7.setopt(ch7.POSTFIELDS, "orderno=" + input_obj.get_text() + "&adminid=" + admin_id)
            ch7.setopt(pycurl.TIMEOUT, out_time)
            ch7.perform()
            ret7 = buffer_con7.getvalue()
            buffer_con7.close()
            ch7.close()
            ret7 = str(ret7, encoding="utf-8")
            print("ret7={}".format(ret7))
            json_ret7 = json.loads(ret7)
            if json_ret7['ret'] == '1':
                continue

            order_info = {'factorynumber': input_obj.get_text(), 'ordername': ordername[0:2],
                          'buyaddress': input_obj.find_parent().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()}
            order_info['province'] = input_obj.find_parent().find_parent().find('span', id=re.compile('aaaa.App_TodoList_DetailCompView.TextView3')).text.strip()
            order_info['city'] = input_obj.find_parent().find_parent().find('span', id=re.compile('aaaa.App_TodoList_DetailCompView.TextView4')).text.strip()
            order_info['county'] = input_obj.find_parent().find_parent().find('span', id=re.compile('aaaa.App_TodoList_DetailCompView.TextView5')).text.strip()
            print("order_info={}".format(order_info))
            # 搜索工单
            form_str0 = strkey + '&SAPEVENTQUEUE=InputField_Change%EE%80%82Id%EE%80%84aaaa.App_TodoList_DetailCompView.Table_0%3A2147483641%EE%80%85Value%EE%80%84' + input_obj.get_text() + '%EE%80%83%EE%80%82Delay%EE%80%84full%EE%80%83%EE%80%82urEventName%EE%80%84INPUTFIELDCHANGE%EE%80%83%EE%80%81InputField_Enter%EE%80%82Id%EE%80%84aaaa.App_TodoList_DetailCompView.Table_0%3A2147483641%EE%80%83%EE%80%82ClientAction%EE%80%84submit%EE%80%83%EE%80%82urEventName%EE%80%84Enter%EE%80%83%EE%80%81Form_Request%EE%80%82Id%EE%80%84...form%EE%80%85Async%EE%80%84false%EE%80%85FocusInfo%EE%80%84%40%7B%22iCursorPosX%22%3A%2010%2C%20%22iSelectionStart%22%3A%20-1%2C%20%22iSelectionEnd%22%3A%20-1%2C%20%22bNavigation%22%3A%20false%2C%20%22sFocussedId%22%3A%20%22aaaa.App_TodoList_DetailCompView.Table_0%3A2147483641%22%2C%20%22sApplyControlId%22%3A%20%22aaaa.App_TodoList_DetailCompView.Table_0%3A2147483641%22%7D%EE%80%85Hash%EE%80%84%EE%80%85DomChanged%EE%80%84false%EE%80%85IsDirty%EE%80%84false%EE%80%83%EE%80%82EnqueueCardinality%EE%80%84single%EE%80%83%EE%80%82%EE%80%83'
            ch7 = pycurl.Curl()
            buffer_con7 = BytesIO()
            ch7.setopt(ch7.WRITEFUNCTION, buffer_con7.write)
            ch7.setopt(ch7.URL, url)
            ch7.setopt(ch7.COOKIE, cookie)
            ch7.setopt(ch7.POST, 1)
            ch7.setopt(ch7.POSTFIELDS, form_str0)
            ch7.setopt(ch7.USERAGENT,
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 "
                       "Safari/537.36")
            ch7.setopt(ch7.TIMEOUT, out_time)
            ch7.perform()
            buffer_con7.close()
            ch7.close()
            # 点击工单查看详情
            form_str = strkey + '&SAPEVENTQUEUE=Link_Activate%EE%80%82Id%EE%80%84' + input_obj.get(
                "id") + '%EE%80%85Ctrl%EE%80%84false%EE%80%85Shift%EE%80%84false%EE%80%83%EE%80%82ClientAction%EE%80%84submit%EE%80%83%EE%80%82ContextPath%EE%80%84Et_Todo_List.0%EE%80%85urEventName%EE%80%84LINKCLICK%EE%80%83%EE%80%81Form_Request%EE%80%82Id%EE%80%84...form%EE%80%85Async%EE%80%84false%EE%80%85FocusInfo%EE%80%84%40%7B%22sFocussedId%22%3A%20%22' + input_obj.get(
                "id") + '%22%7D%EE%80%85Hash%EE%80%84%EE%80%85DomChanged%EE%80%84false%EE%80%85IsDirty%EE%80%84false%EE%80%83%EE%80%82EnqueueCardinality%EE%80%84single%EE%80%83%EE%80%82%EE%80%83'
            ch4 = pycurl.Curl()
            buffer_con4 = BytesIO()
            ch4.setopt(ch4.WRITEFUNCTION, buffer_con4.write)
            ch4.setopt(ch4.URL, url)
            ch4.setopt(ch4.COOKIE, cookie)
            ch4.setopt(ch4.POST, 1)
            ch4.setopt(ch4.POSTFIELDS, form_str)
            ch4.setopt(ch4.USERAGENT,
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 "
                       "Safari/537.36")
            ch4.setopt(ch4.TIMEOUT, out_time)
            ch4.perform()
            detail_html = buffer_con4.getvalue()
            detail_html = str(detail_html, encoding="utf-8")
            buffer_con4.close()
            ch4.close()
            orderdetail_dom = BeautifulSoup(re.findall(r'<table.*?>(.*)</table>', detail_html)[0], "html.parser")
            # print(orderdetail_dom)
            base_key = orderdetail_dom.select(".urBtnStd")[0].get("id")
            base_key1 = base_key.split(".")
            # 返回工单列表页
            form_str1 = strkey + '&SAPEVENTQUEUE=Button_Press%EE%80%82Id%EE%80%84' + base_key1[0] + '.' + base_key1[
                1] + '.Btn_Close' + '%EE%80%83%EE%80%82ClientAction%EE%80%84submit%EE%80%83%EE%80%82urEventName%EE%80%84BUTTONCLICK%EE%80%83%EE%80%81Form_Request%EE%80%82Id%EE%80%84...form%EE%80%85Async%EE%80%84false%EE%80%85FocusInfo%EE%80%84%40%7B%22sFocussedId%22%3A%20%22' + \
                        base_key1[0] + '.' + base_key1[
                            1] + '.Btn_Close' + '%22%7D%EE%80%85Hash%EE%80%84%EE%80%85DomChanged%EE%80%84false%EE%80%85IsDirty%EE%80%84false%EE%80%83%EE%80%82EnqueueCardinality%EE%80%84single%EE%80%83%EE%80%82%EE%80%83'
            ch5 = pycurl.Curl()
            buffer_con5 = BytesIO()
            ch5.setopt(ch5.WRITEFUNCTION, buffer_con5.write)
            ch5.setopt(ch5.URL, url)
            ch5.setopt(ch5.COOKIE, cookie)
            ch5.setopt(ch5.POST, 1)
            ch5.setopt(ch5.POSTFIELDS, form_str1)
            ch5.setopt(ch5.USERAGENT,
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 "
                       "Safari/537.36")
            ch5.setopt(ch5.TIMEOUT, out_time)
            ch5.perform()
            buffer_con5.close()
            ch5.close()
            order_info['repairtime'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.Zzfld00003J').get(
                "value")

            if order_info['ordername'] == '安装':
                order_info['orderstatus'] = orderdetail_dom.find(
                    id=base_key1[0] + '.' + base_key1[1] + '.DropDownByKey1').get(
                    "value")
                order_info['machinetype'] = orderdetail_dom.find(
                    id=base_key1[0] + '.' + base_key1[1] + '.DropDownByKey9').get(
                    "value")
                order_info['mobile'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.InputField7').get(
                    "value")
                order_info['address'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.InputField8').get(
                    "value")
                order_info['buydate'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.Zzfld00002Y').get(
                    "value")
            elif order_info['ordername'] == '维修':
                order_info['orderstatus'] = orderdetail_dom.find(
                    id=base_key1[0] + '.' + base_key1[1] + '.DropDownByKey').get(
                    "value")
                order_info['machinetype'] = orderdetail_dom.find(
                    id=base_key1[0] + '.' + base_key1[1] + '.DropDownByKey7').get(
                    "value")
                order_info['mobile'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.InputField7').get(
                    "value")
                order_info['address'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.InputField8').get(
                    "value")
                order_info['buydate'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.Zzfld00002Y').get(
                    "value")
            else:
                order_info['orderstatus'] = orderdetail_dom.find(
                    id=base_key1[0] + '.' + base_key1[1] + '.DropDownByKey').get(
                    "value")
                order_info['machinetype'] = orderdetail_dom.find(
                    id=base_key1[0] + '.' + base_key1[1] + '.DropDownByKey1').get(
                    "value")
                order_info['mobile'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.InputField1').get(
                    "value")
                order_info['address'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.InputField2').get(
                    "value")
                order_info['buydate'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.Zzfld00001H').get(
                    "value")

            order_info['originname'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.Zzfld00001K').get(
                "value")
            order_info['username'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.CustomerName').get(
                "value")

            order_info['sn'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.Zzfld00001R').get("value")
            order_info['ordertime'] = orderdetail_dom.find(id=base_key1[0] + '.' + base_key1[1] + '.Created_At').get(
                "value")
            order_info['description'] = orderdetail_dom.find(
                id=base_key1[0] + '.' + base_key1[1] + '.TextEdit').get_text()
            order_info['companyid'] = 9
            order_info['machinebrand'] = '华帝'
            order_info['adminid'] = admin_id
            order_list[k1] = order_info
            print("hd--> order_info >>> {}".format(order_info))
            k1 = k1 + 1
        ch6 = pycurl.Curl()
        buffer_con6 = BytesIO()
        ch6.setopt(ch6.WRITEFUNCTION, buffer_con6.write)
        ch6.setopt(ch6.URL, bjdomain + "/Api/Climborder/addorder")
        ch6.setopt(ch6.POST, 1)
        ch6.setopt(ch6.POSTFIELDS, "data=" + json.dumps(order_list))
        ch6.setopt(ch6.TIMEOUT, out_time)
        ch6.perform()
        buffer_con6.close()
        ch6.close()
        print("hd--> total_orders end  >>> ")
        return {'code': 1, 'msg': "get_orders success"}
    except Exception as e:
        print("获取工单详情失败：" + str(e))
        # add_api_log(bjdomain, mobile, '9', str(e), 'get_orders')
        return {'code': 0, 'msg': str(e)}


def transfer_order(baseurl, cookie_str, adminid, bjdomain,login_account):
    try:
        ch1 = pycurl.Curl()
        buffer_con1 = BytesIO()
        ch1.setopt(ch1.WRITEFUNCTION, buffer_con1.write)
        ch1.setopt(ch1.URL, baseurl + "/irj/portal")
        ch1.setopt(ch1.COOKIE, cookie_str)
        ch1.setopt(ch1.REFERER, baseurl + "/irj/portal")
        ch1.setopt(ch1.USERAGENT,
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 "
                   "Safari/537.36")
        ch1.setopt(ch1.TIMEOUT, out_time)
        ch1.perform()
        ret = buffer_con1.getvalue()
        ret = str(ret, encoding="utf-8")
        buffer_con1.close()
        ch1.close()
        key = re.findall('afpVerifierKey =(.*);', ret)
        print("hd--> afpVerifierKey = ", key)
        Key1 = key[0].split(";")
        afpVerifierKey = Key1[0].strip()
        jsonCacheTimeStampsRep = re.findall('jsonCacheTimeStampsRep =(.*);', ret)
        jsonCacheTimeStampsRep1 = jsonCacheTimeStampsRep[0].split(";")
        jsonCacheTimeStampsRep2 = jsonCacheTimeStampsRep1[0].strip()
        jsonCacheTimeStampsRep2 = json.loads(eval(jsonCacheTimeStampsRep2))


        # 得到NavigationTarget
        target_url = baseurl + "/AFPServlet/NavigationServlet?action=getSelectedPathTree&mode=nogzip&supportInitialNavNodesFilter=true&targetNodeId=&pathname=%2Firj%2Fportal&sap-ep-inp=" + \
                     jsonCacheTimeStampsRep2['sap-ep-inp'] + "&sap-ep-nh=" \
                     + jsonCacheTimeStampsRep2['sap-ep-nh'] + "&sap-ep-pp=" + jsonCacheTimeStampsRep2[
                         'sap-ep-pp'] + "&sap-ep-ul=" + jsonCacheTimeStampsRep2['sap-ep-ul'] + "&sap-ep-ur=" + \
                     jsonCacheTimeStampsRep2['sap-ep-ur'] + "&afpVerifierKey=" + afpVerifierKey[1:-1]
        ch = pycurl.Curl()
        buffer_con = BytesIO()
        ch.setopt(ch.WRITEFUNCTION, buffer_con.write)
        ch.setopt(ch.URL, target_url)
        ch.setopt(ch.COOKIE, cookie_str)
        ch.setopt(ch.REFERER, baseurl + "/irj/portal")
        ch.setopt(ch.TIMEOUT, out_time)
        ch.perform()
        ret1 = buffer_con.getvalue()
        ret1 = str(ret1, encoding="utf-8")
        buffer_con.close()
        ch.close()
        ret_info1 = json.loads(ret1)
        navurl = ret_info1['rootNodes'][0]['childNodes'][0]['id']
        print("hd--> navurl = ", navurl)
        winid = 'WID1571725374585'
        index_url = baseurl + "/irj/servlet/prt/portal/prteventname/Navigate/prtroot/pcd!3aportal_content" \
                              "!2fevery_user!2fgeneral!2fdefaultAjaxframeworkContent!2fcom.sap.portal.contentarea?windowId=" + winid \
                    + "&supportInitialNavNodesFilter=true "
        ch2 = pycurl.Curl()
        buffer_con2 = BytesIO()
        ch2.setopt(ch2.WRITEFUNCTION, buffer_con2.write)
        header1 = ['Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36']
        ch2.setopt(ch2.HTTPHEADER, header1)
        ch2.setopt(ch2.URL, index_url)
        ch2.setopt(ch2.COOKIE, cookie_str)
        ch2.setopt(ch2.REFERER, baseurl + "/irj/portal")
        ch2.setopt(ch2.POST, 1)
        ch2.setopt(ch2.POSTFIELDS, "NavigationTarget=" + navurl)
        ch2.setopt(ch2.WRITEFUNCTION, buffer_con2.write)
        ch2.setopt(ch2.TIMEOUT, out_time)
        ch2.perform()
        ret2 = buffer_con2.getvalue()
        buffer_con2.close()
        ch2.close()
        ret2 = str(ret2, encoding="utf-8")
        loginpage = BeautifulSoup(ret2, "html.parser")
        input_html = loginpage.select('input')

        search_url = baseurl + "/webdynpro/resources/sap.com/pb/PageBuilder;jsessionid=" + get_jid(cookie_str)
        post_data = {'sap-ext-sid': input_html[0].get('value'), 'sap-wd-cltwndid': input_html[1].get('value'),
                     'sap-wd-tstamp': input_html[2].get('value'), 'PagePath': input_html[3].get('value'),
                     'sap-wd-app-namespace': input_html[4].get('value'), 'sap-ep-version': input_html[5].get('value'),
                     'sap-locale': input_html[6].get('value'), 'sap-accessibility': input_html[7].get('value'),
                     'sap-rtl': input_html[8].get('value'), 'sap-explanation': input_html[9].get('value'),
                     'sap-cssurl': input_html[10].get('value'), 'sap-cssversion': input_html[11].get('value'),
                     'sap-epcm-guid': input_html[12].get('value'),
                     'com.sap.portal.reserved.wd.pb.restart': input_html[13].get('value'),
                     'DynamicParameter': input_html[14].get('value'),
                     'supportInitialNavNodesFilter': input_html[15].get('value'),
                     'NavigationTarget': input_html[16].get('value')}
        ch3 = pycurl.Curl()
        buffer_con3 = BytesIO()
        ch3.setopt(ch3.WRITEFUNCTION, buffer_con3.write)
        ch3.setopt(ch3.URL, search_url)  # 传入url
        ch3.setopt(ch3.COOKIE, cookie_str)  # 请求发送cookie源文件
        ch3.setopt(ch3.POST, 1)
        ch3.setopt(ch3.POSTFIELDS, url_encoder(post_data))
        ch3.setopt(ch3.USERAGENT,
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 "
                   "Safari/537.36")
        ch3.setopt(ch3.TIMEOUT, out_time)
        ch3.perform()
        order_html = buffer_con3.getvalue()
        order_html = str(order_html, encoding="utf-8")
        buffer_con3.close()
        ch3.close()
        orderdata_dom1 = BeautifulSoup(order_html, "html.parser")
        total_data = orderdata_dom1.find_all(id='aaaa.App_TodoList_DetailCompView.Table_0')[0].get("lsdata")
        total_data = eval(total_data)
        print("hd--> total_orders = ",total_data)
        total_pages = math.ceil(total_data[2] / 20)
        search_url2 = baseurl + "/webdynpro/resources/sap.com/pb/PageBuilder"
        base_str = 'sap-ext-sid=' + orderdata_dom1.find(attrs={"name": "sap-ext-sid"}).get("value") \
                   + '&sap-wd-cltwndid=' + winid + '&sap-wd-norefresh=X&sap-wd-secure-id=' \
                   + orderdata_dom1.find(attrs={"name": "sap-wd-secure-id"}).get("value")
        get_orders_respon = get_orders(orderdata_dom1, search_url2, cookie_str, base_str, adminid, bjdomain,login_account)
        if get_orders_respon and get_orders_respon["code"] == 0:
            return  get_orders_respon
        if total_pages > 1:  # 目前一页显示20条记录
            n = 0
            while n < total_pages:
                n = n + 1
                if n == 10:
                    break
                print("查询第" + str(n) + "页数据:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                form_str5 = base_str + '&SAPEVENTQUEUE=SapTable_VerticalScroll%EE%80%82Id%EE%80%84aaaa.App_TodoList_DetailCompView' \
                                       '.Table_0%EE%80%85FirstVisibleItemIndex%EE%80%84' + str(n * 20 + 1) + \
                            '%EE%80%85Action%EE%80%84DIRECT%EE%80%85CellId%EE%80%84%EE%80%85AccessType%EE%80%84SCROLLBAR%EE' \
                            '%80%85SelectionFollowFocus%EE%80%84false%EE%80%85Shift%EE%80%84false%EE%80%85Ctrl%EE%80%84false' \
                            '%EE%80%85Alt%EE%80%84false%EE%80%83%EE%80%82ClientAction%EE%80%84submit%EE%80%83%EE%80' \
                            '%82urEventName%EE%80%84VerticalScroll%EE%80%83%EE%80%81Form_Request%EE%80%82Id%EE%80%84...form' \
                            '%EE%80%85Async%EE%80%84false%EE%80%85FocusInfo%EE%80%84%40%7B%7D%EE%80%85Hash%EE%80%84%EE%80' \
                            '%85DomChanged%EE%80%84false%EE%80%85IsDirty%EE%80%84false%EE%80%83%EE%80%82EnqueueCardinality%EE' \
                            '%80%84single%EE%80%83%EE%80%82%EE%80%83'
                ch8 = pycurl.Curl()
                buffer_con8 = BytesIO()
                ch8.setopt(ch8.WRITEFUNCTION, buffer_con8.write)
                ch8.setopt(ch8.URL, search_url2)
                ch8.setopt(ch8.COOKIE, cookie_str)
                ch8.setopt(ch8.POST, 1)
                ch8.setopt(ch8.POSTFIELDS, form_str5)
                ch8.setopt(ch8.USERAGENT,
                           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 "
                           "Safari/537.36")
                ch8.setopt(ch8.TIMEOUT, out_time)
                ch8.perform()
                order_html2 = buffer_con8.getvalue()
                order_html2 = str(order_html2, encoding="utf-8")
                buffer_con8.close()
                ch8.close()
                orderdata_dom2 = BeautifulSoup(re.findall(r'<table.*?>(.*)</table>', order_html2)[0], "html.parser")
                get_orders_respon = get_orders(orderdata_dom2, search_url2, cookie_str, base_str, adminid, bjdomain,login_account)
                if get_orders_respon and get_orders_respon["code"] == 0:
                    return get_orders_respon
        return {'code': 1, 'msg': "success"}

    except Exception as e2:
        print("查询代办列表失败：", e2)
        # add_api_log(bjdomain, login_account, '9', str(e2), 'transfer_order')
        return {'code': 0, 'msg': str(e2)}


if __name__ == '__main__':
    url = 'http://crm.vatti.com.cn:8180'
    loginresult = login_hd(url=url,username='101393-4', pwd='ffhc2821')
    if loginresult['code'] == 1:
        grap_res = transfer_order(url, loginresult['element'], "24", 'http://yxgtest.bangjia.me', '18667141169')
        if grap_res and grap_res["code"] == 0:
            print("华帝抓单异常数据===>", grap_res)
    print("华帝抓单成功")
