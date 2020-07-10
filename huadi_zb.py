# -*- coding: utf-8 -*-
from urllib.parse import urlencode

import requests
import json
from bs4 import BeautifulSoup
import re
from datetime import date, timedelta, datetime
from Util import Util


class HDScrap(Util):
    def __init__(self, username='01007544', pwd='160324', baseurl="http://cc.vatti.com.cn:8180", adminid='3',
                 bjdomain='http://yxgtest.bangjia.me', companyid='9'):
        self.session = requests.Session()
        self.username = username
        self.passwd = pwd
        self.baseurl = baseurl
        self.codeFaultTimes = 0
        self.loginFaultTimes = 0
        self.adminid = adminid
        self.bjdomain = bjdomain
        self.datasuccess = {'code': 1, 'msg': '抓单成功', 'element': ''}
        self.datafail = {'code': 0, 'msg': '登录失败,请检查账号密码是否正确'}
        self.isSucess = False
        self.companyid = companyid
        self.mainurl = None
        self.headers = {'Content-type': 'text/html', 'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,pt;q=0.6', 'Connection': 'keep-alive',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,'
                                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Host': "cc.vatti.com.cn:8180",
                        'Origin': baseurl,
                        # 'User-Agent': agent,
                        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/79.0.3945.88 Safari/537.36"}

    def get_lsdata(self, element):
        data = element["lsdata"]
        data = data.replace(r"true", '1')
        data = data.replace(r"false", '0')
        return eval(data)[2]

    def get_value(self, element):
        return element["value"]

    def loginHd(self):
        loginurl = self.baseurl + '/sap/bc/bsp/sap/crm_ui_start/default.htm?sap-client=800&sap-language=ZH'
        print("url=" + loginurl + ",passwd=" + self.passwd)
        self.headers['Referer'] = loginurl
        loginRes = self.session.get(loginurl, headers=self.headers)
        loginRes.encoding = 'utf-8'
        bsObj = BeautifulSoup(loginRes.text, features="lxml")
        # print("=========================")
        processname = self.get_value(bsObj.find("input", {"name": "sap-system-login"}))
        sap_client = self.get_value(bsObj.find("input", {"id": "sap-client"}))
        loginxsrf = bsObj.find("input", {"name": "sap-login-XSRF"})["value"]
        params = {"FOCUS_ID": self.get_value(bsObj.find("input", {"id": "FOCUS_ID"})),
                  "sap-system-login-oninputprocessing": processname,
                  "sap-system-login": processname,
                  "sap-login-XSRF": loginxsrf,
                  "sysid": self.get_lsdata(bsObj.find("input", {"id": "sysid"})),
                  "sap-client": sap_client,
                  "sap-user": self.username, "sap-password": self.passwd,
                  "SAPEVENTQUEUE": "Form_Submit~E002Id~E004SL__FORM~E003~E002ClientAction~E004submit~E005ActionUrl~E004"
                                   "~E005ResponseData~E004full~E005PrepareScript~E004~E003~E002~E003",
                  "sap-language": self.get_value(bsObj.find("input", {"id": "sap-language"})),
                  "sap-language-dropdown": self.get_value(bsObj.find("input", {"id": "sap-language-dropdown"}))}
        self.headers['Content-type'] = "application/x-www-form-urlencoded"
        checkRes = self.session.post(loginurl, data=params, headers=self.headers)
        self.selectrole()
        return self.checkstatus(checkRes)

    def checkstatus(self, response, callback=None):
        bsObj = self.getsoup(response)
        nextbtn = bsObj.find_all("a", {"id": "SESSION_QUERY_CONTINUE_BUTTON"})
        logonbtn = bsObj.find_all("a", {"id": "LOGON_BUTTON"})
        # 如果账号密码错误 或者其他问题，直接返回
        if response.status_code != 200:
            return self.datafail
        # 如果有其他账户在登陆，点击继续
        elif nextbtn:
            return self.continuelogon()
        elif logonbtn:
            return self.datafail
        if callback:
            return callback(bsObj)
        return self.datasuccess

    def continuelogon(self, callback=None):
        """ 点击继续，踢掉其他用户继续当前会话 """
        print("有其他账户登陆，点击继续")
        params = {"FOCUS_ID": "SESSION_QUERY_CONTINUE_BUTTON",
                  "sap-system-login-oninputprocessing": "onSessionQuery",
                  "sap-system-login": "onSessionQuery",
                  "sap-client": '800',
                  "SAPEVENTQUEUE": "Form_Submit~E002Id~E004SL__FORM~E003~E002ClientAction~E004submit~E005ActionUrl~E004"
                                   "~E005ResponseData~E004full~E005PrepareScript~E004~E003~E002~E003",
                  "sap-language": 'ZH',
                  "delete-session-cb": 'X', "delete_session": 'X'
                  }
        self.headers['Content-type'] = "application/x-www-form-urlencoded"
        url = self.baseurl + '/sap/bc/bsp/sap/crm_ui_start/default.htm'
        checkRes = self.session.post(url, data=params, headers=self.headers)
        # print(checkRes.status_code)
        if checkRes.status_code != 200:
            return self.datafail
        result = self.selectrole()
        if callback:
            return callback()
        return result

    def selectrole(self):
        # print('=========================选择角色')
        url = self.baseurl + "/sap/bc/bsp/sap/crm_ui_frame/main.htm?sap-client=800&sap-language=ZH&sap-domainRelax" \
                             "=min&saprole=ZIC_AGENT_08&sapouid=50000265&sapoutype=S"
        roleRes = self.session.get(url, headers=self.headers)
        if roleRes.status_code != 200:
            return self.datafail
        return self.datasuccess

    def getsoup(self, response):
        # print(response.status_code)
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, features="lxml")

    def transfer_order(self, statuscode=None):
        # print('=========================loadFrame1 加载左边的动作栏')
        url = self.mainurl
        if not url or len(url) <= 1:
            url = self.baseurl + "/sap/bc/bsp/sap/crm_ui_frame/BSPWDApplication.do?sap-client=800&sap-language=ZH&sap" \
                                 "-domainrelax=min&saprole=ZIC_AGENT_08&sapouid=50000265&sapoutype=S"
        self.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        del self.headers['Content-type']
        actionRes = self.session.get(url, headers=self.headers)
        # print(actionRes.text)
        result = self.checkstatus(actionRes)
        if result['code'] == 1:
            try:
                bsObj = self.getsoup(actionRes)
                if not bsObj:
                    return self.datafail
                sercureid = self.get_value(bsObj.find("input", {"id": "wcf-secure-id"}))
                cb_flash = self.get_value(bsObj.find("input", {"id": "callbackFlashIslands"}))
                cb_light = self.get_value(bsObj.find("input", {"id": "callbackSilverlightIslands"}))
                data = {"data": json.dumps(self.loadallsearch(sercureid, cb_flash, cb_light, statuscode))}
                if statuscode:
                    data['vatti_type'] = 1
                # print("transfer_order:", data)
                result = requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
                # print(result)
            except Exception as e:
                print("transfer_order exception", e)
                return self.datafail
            return self.datasuccess
        else:
            return self.datafail

    def loadsearch(self, sercureid, cb_flash, cb_light):
        # print('=========================loadsearch 加载工单查询初始页面')
        params = {"callbackFlashIslands": cb_flash,
                  "callbackSilverlightIslands": cb_light,
                  "htmlbevt_frm": "myFormId",
                  "htmlbevt_cnt": "0",
                  "onInputProcessing": "htmlb",
                  "htmlbevt_ty": "thtmlb:link:click:0",
                  "htmlbevt_id": "ZSRV-02-SR",
                  "htmlbevt_oid": "C6_W29_V30_ZSRV-01-SR",
                  "thtmlbKeyboardFocusId": "C6_W29_V30_ZSRV-01-SR",
                  "sap-ajaxtarget": "C1_W1_V2_C6_W29_V30_MainNavigationLinks.do",
                  "sap-ajax_dh_mode": "AUTO",
                  "wcf-secure-id": sercureid,
                  "PREFIX_ID": "C9_W36_V37_",
                  "LTX_PREFIX_ID": "C1_W1_V2_",
                  "sap-ajax_request": "X",
                  "C4_W23_V24_V25_tv1_multiParameter": "0////0////0////0",
                  "C8_W34_V35_RecentObjects_isExpanded": "yes",
                  "C4_W23_V24_V25_tv1_isCellerator": "TRUE",
                  "C4_W23_V24_V25_tv1_isNavModeActivated": "TRUE",
                  "C4_W23_V24_V25_tv1_filterApplied": "FALSE",
                  "C4_W23_V24_V25_tv1_editMode": "NONE",
                  "C4_W23_V24_V25_tv1_firstTimeRendering": "NO",
                  "C9_W36_V37_POLLFREE_ALERTS": "{&#34;Alerts&#34;:[]}",
                  "C4_W23_V24_V25_tv1_configHash": "827DEA574484325768AF0E54A8EB7CBF8083ED01",
                  "C3_W18_V19_V21_searchcustomer_struct.reltyp": "BUR001",
                  "C4_W23_V24_V25_tv1_bindingString": "//CUSTOMERS/Table",
                  "C13_W47_V48_SearchMenuAnchor1": "UP"
                  }
        sap = re.findall(re.compile(r'[(](.*?)[)]', re.S), params['callbackFlashIslands'])[0]
        url = self.baseurl + "/sap(%s)/bc/bsp/sap/crm_ui_frame/BSPWDApplication.do" % sap
        print("loadsearch url={}".format(url))
        self.mainurl = url
        self.headers['Content-type'] = "application/x-www-form-urlencoded"
        self.headers['Referer'] = url
        # 该参数代表了是否异步加载，如果加了这个选项，会只能接受到建议的网页，导致解析出错，浪费2天时间
        # self.headers['X-Requested-With'] = "XMLHttpRequest"
        self.headers['Accept'] = "*/*"
        roleRes = self.session.post(url, data=params, headers=self.headers)
        # print(roleRes.text)
        return self.getsoup(roleRes), params

    def loadallsearch(self, sercureid, cb_flash, cb_light, statuscode=None):
        soup, params = self.loadsearch(sercureid, cb_flash, cb_light)
        confighash = str(soup.find("input", {"id": "C17_W61_V62_V64_ResultTable_configHash"})["value"])
        order = list(self.search(confighash, params, 0, statuscode=statuscode))
        return order

    def search(self, confighash, _params, page, totalcount=100, pagecount=50, statuscode=None):
        # print('=========================loadsearch 搜索', '增值工单' if not statuscode else '安装工单')
        target = "C1_W1_V2_C1_W1_V2_V3_C17_W61_V62_SearchViewSet.do" if page == 0 else "C1_W1_V2_C1_W1_V2_V3_C17_W61_V62_C17_W61_V62_V64_advancedsrl.do"
        oid = "C17_W61_V62_Searchbtn" if page == 0 else "C17_W61_V62_V64_ResultTable"
        focusid = "C17_W61_V62_Searchbtn" if page == 0 else "C17_W61_V62_V64_ResultTable_pag_pg-%d" % page
        params = {
            "callbackFlashIslands": _params['callbackFlashIslands'],
            "callbackSilverlightIslands": _params['callbackSilverlightIslands'],
            "htmlbevt_frm": "myFormId",
            "htmlbevt_cnt": "0" if page == 0 else "1", "onInputProcessing": "htmlb",
            "htmlbevt_ty": "htmlb:button:click:0" if page == 0 else "thtmlb:tableView:navigate:null",
            "htmlbevt_id": "SEARCH_BTN" if page == 0 else "tvNavigator",
            "sap-ajax_dh_mode": "AUTO",
            "wcf-secure-id": _params['wcf-secure-id'], "PREFIX_ID": "C9_W36_V37_",
            "LTX_PREFIX_ID": "C1_W1_V2_", "sap-ajax_request": "X",
            "crmFrwScrollXPos": "0", "crmFrwScrollYPos": "267",
            "crmFrwOldScrollXPos": "0", "crmFrwOldScrollYPos": "267", "thtmlbScrollAreaWidth": "0",
            "thtmlbScrollAreaHeight": "0", "C13_W47_V48_SearchMenuAnchor1": "UP",
            'htmlbevt_oid': oid, 'thtmlbKeyboardFocusId': focusid,
            'sap-ajaxtarget': target, 'currentDate': datetime.now().year,
            'C17_W61_V62_V64_ResultTable_configHash': confighash,
            'C17_W61_V62_V64_ResultTable_multiParameter': "0////0////0////0",
            'C17_W61_V62_V64_ResultTable_bindingString': "//BTQRSrvOrd/Table",
            'C17_W61_V62_V64_ResultTable_sortValue': 'CREATED_AT#:#desc#!#',
            'C17_W61_V62_V63_btqsrvord_max_hits': "9" if statuscode else "9",  # 一次查询最大多少条
            'C17_W61_V62_thtmlbShowSearchFields': "true",
            'C17_W61_V62_V64_ResultTable_isNavModeActivated': "TRUE",
            'C17_W61_V62_V64_ResultTable_filterApplied': "FALSE", 'C17_W61_V62_V64_ResultTable_isCellerator': "TRUE",
            'C17_W61_V62_V64_ResultTable_editMode': "NONE",
            'C17_W61_V62_V64_ResultTable_visibleFirstRow': str(1 + page * 10),
            "C17_W61_V62_V63_btqsrvord_parameters[1].FIELD": "POSTING_DATE",
            "C17_W61_V62_V63_btqsrvord_parameters[1].OPERATOR": "GT" if not statuscode else "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[1].VALUE1": (date.today() - timedelta(days=1)).strftime("%Y.%m.%d"),
            "C17_W61_V62_V63_btqsrvord_parameters[1].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[2].FIELD": "ZZFLD000057",
            "C17_W61_V62_V63_btqsrvord_parameters[2].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[2].VALUE1": "",
            "C17_W61_V62_V63_btqsrvord_parameters[2].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[3].FIELD": "ZZFLD000063",
            "C17_W61_V62_V63_btqsrvord_parameters[3].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[3].VALUE1": "",
            "C17_W61_V62_V63_btqsrvord_parameters[3].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[4].FIELD": "ZZFLD00005P",
            "C17_W61_V62_V63_btqsrvord_parameters[4].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[4].VALUE1": "01" if not statuscode else "",  # 工单来源是HD-华帝
            "C17_W61_V62_V63_btqsrvord_parameters[4].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[5].FIELD": "OBJECT_ID",
            "C17_W61_V62_V63_btqsrvord_parameters[5].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[5].VALUE1": "",
            "C17_W61_V62_V63_btqsrvord_parameters[5].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[6].FIELD": "PROCESS_TYPE",
            "C17_W61_V62_V63_btqsrvord_parameters[6].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[6].VALUE1": "ZIC6" if not statuscode else "ZIC3",  # 工单类型为 增值服务单
            "C17_W61_V62_V63_btqsrvord_parameters[6].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[7].FIELD": "ZZFLD00003J",
            "C17_W61_V62_V63_btqsrvord_parameters[7].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[7].VALUE1": "",
            "C17_W61_V62_V63_btqsrvord_parameters[7].VALUE2": "",
            # "C17_W61_V62_V63_btqsrvord_parameters[8].FIELD": "STATUS_COMMON",
            # "C17_W61_V62_V63_btqsrvord_parameters[8].OPERATOR": "EQ",
            # "C17_W61_V62_V63_btqsrvord_parameters[8].VALUE1": "M0002ZSIC0002",  # 状态为工单提交
            # "C17_W61_V62_V63_btqsrvord_parameters[8].VALUE2": "",
            # "C17_W61_V62_V63_btqsrvord_parameters[9].FIELD": "ZZFLD000062",
            # "C17_W61_V62_V63_btqsrvord_parameters[9].OPERATOR": "EQ",
            # "C17_W61_V62_V63_btqsrvord_parameters[9].VALUE1": "",
            # "C17_W61_V62_V63_btqsrvord_parameters[9].VALUE2": "",
            'C17_W61_V62_V64_ResultTable_firstTimeRendering': "NO",
            "C9_W36_V37_POLLFREE_ALERTS": "{&#34;Alerts&#34;:[]}",
            "C17_W61_V62_V64_ResultTable_rowCount": "0" if page == 0 else str(totalcount)
        }
        # if statuscode:
        #     params["C17_W61_V62_V63_btqsrvord_parameters[8].FIELD"] = "STATUS_COMMON"
        #     params["C17_W61_V62_V63_btqsrvord_parameters[8].OPERATOR"] = "EQ"
        #     params["C17_W61_V62_V63_btqsrvord_parameters[8].VALUE1"] = statuscode
        #     params["C17_W61_V62_V63_btqsrvord_parameters[8].VALUE2"] = ""
        if page != 0:
            params['htmlbevt_par1'] = "page:%d,%d,%d,%d,P" % (page + 1, 1 + page * pagecount, pagecount, totalcount)
        sap = re.findall(re.compile(r'[(](.*?)[)]', re.S), params['callbackFlashIslands'])[0]
        url = self.baseurl + "/sap(%s)/bc/bsp/sap/crm_ui_frame/BSPWDApplication.do" % sap
        self.headers['Content-type'] = "application/x-www-form-urlencoded"
        self.headers['Referer'] = url
        print("page={},totalcount={},url={},headers={}".format(page, totalcount, url, self.headers))
        roleRes = self.session.post(url, data=params, headers=self.headers)
        bsObj = self.getsoup(roleRes)
        # if statuscode:
        #     print("search result={}".format(roleRes.text))
        resulttable = bsObj.find("table", {"id": "C17_W61_V62_V64_ResultTable_TableHeader"}).find("tbody")
        totalcount = int(bsObj.find("input", {"id": "C17_W61_V62_V64_ResultTable_rowCount"})["value"])
        isall = (page + 1) * pagecount >= totalcount
        print("totalcount=%d" % totalcount + ",page=%d" % page + ",isallloaded=%d" % isall)
        if resulttable:
            yield from self.parseorderlist(resulttable.find_all("tr"), url, params, statuscode)
            if not isall:
                yield from self.search(confighash, _params, page + 1, totalcount, pagecount, statuscode)

    def parseorderlist(self, trlist, url, params, statuscode):
        for tr in trlist:
            tablecolumns = tr.find_all("td")
            if tr and len(tablecolumns) > 2:
                data = self.parseorder(tablecolumns, statuscode)
                if data:
                    yield from self.orderdetail(data, url, params, statuscode)

    def finda(self, element):
        return element.find("a").text.strip()

    def findspan(self, element):
        return element.find("span").text.strip()

    def isNew(self, data):
        res = requests.post(self.bjdomain + "/Api/Climborder/checkexist",
                            data={"orderno": data['factorynumber'], 'adminid': self.adminid})
        return self.checkBjRes(res)

    def parseorder(self, tablecolumns, statuscode=None):
        try:
            orderno_td = tablecolumns[1]
            name_td = tablecolumns[3]
            data = {}
            orderitem = orderno_td.find("a")
            nameaddress = self.finda(name_td).split(" / ")
            if orderitem and orderitem.has_attr('id'):
                data['oid'] = orderitem["id"]  # 这个是上一个列表中的工单号元素id，下一个页面需要用到
                data['pid'] = name_td.find("a")['id']  # 这个是上一个列表中的用户名元素id，下一个页面需要用到
                data['factorynumber'] = self.finda(orderno_td)
                data['username'] = nameaddress[0]
                data['originname'] = self.findspan(tablecolumns[4])
                data['ordertime'] = self.findspan(tablecolumns[7]).replace(".", '-')
                data['companyid'] = self.companyid
                data['machinebrand'] = "华帝"
                data['orderstatus'] = "工单提交"
                data['adminid'] = self.adminid
                if len(nameaddress) > 1 and "-" in nameaddress[1]:
                    address = nameaddress[1].split("-")
                    if len(address) > 1:
                        data['city'] = address[0]
                        data['county'] = address[1]
                # print("parseorder data=")
                # print(data)
                if data['username']:
                    data['username'] = data['username'].split(" ")[0]
                return data if not statuscode or self.isNew(data) else None
        except Exception as e:
            print("parseorder exception", e)
        return None

    def orderdetail(self, data, url, params, statuscode):
        # print('=========================orderdetail 获取工单详情')
        oid = data['oid']
        params['htmlbevt_ty'] = "thtmlb:link:click:0"
        params['htmlbevt_oid'] = oid
        params['thtmlbKeyboardFocusId'] = oid
        params['htmlbevt_id'] = "HEADEROV"
        params['htmlbevt_cnt'] = "0"
        params['currentDate'] = datetime.now().year
        params['sap-ajaxtarget'] = "C1_W1_V2_C1_W1_V2_V3_C17_W61_V62_C17_W61_V62_V64_advancedsrl.do"
        if 'htmlbevt_par1' in params:
            del params['htmlbevt_par1']
        roleRes = self.session.post(url, data=params, headers=self.headers)
        bsObj = self.getsoup(roleRes)
        if statuscode:
            # print(roleRes.text)
            data['orderstatus'] = "服务完成" if statuscode == "M0010ZSIC0003" else "回访完成"
            data['machinetype'] = bsObj.find("span", {"id": "C19_W69_V72_V75_thtmlb_textView_28"}).text.strip()  # 机器类型
            data['buydate'] = bsObj.find("span",
                                         {"id": "C19_W69_V72_V75_btadminh_ext.zzfld00002y"}).text.strip()  # 购买日期
            data['ordername'] = "安装"
            data['sn'] = bsObj.find("span", {"id": "C19_W69_V72_V75_btadminh_ext.zzfld00001r"}).text.strip()  # 条码
            data['version'] = self.getTableRow(bsObj, "C23_W85_V86_V88_Table_TableHeader",
                                               lambda row: self.finda(row[3]) + "|")  # 产品编号 拼接
            data['machine_dsc'] = self.getTableRow(bsObj, "C23_W85_V86_V88_Table_TableHeader",
                                               lambda row: self.finda(row[6]) + "|")  # 产品编号 拼接
            data = self.getFinishTime(data, url, params)
        else:
            user_tr = bsObj.find("div", {"id": "C19_W69_V72_0003Content"}).find("tbody").find("tr")
            data['mobile'] = user_tr.find('span', id=re.compile('partner_no')).text.strip()
            data['address'] = user_tr.find('span', id=re.compile('address_short')).text.strip()
            data['repairtime'] = bsObj.find("span",
                                            {"id": "C19_W69_V72_V74_btadminh_ext.zzfld00003j"}).text.strip()  # 预约时间
            data['machinetype'] = bsObj.find("span", {"id": "C19_W69_V72_V74_thtmlb_textView_30"}).text.strip()  # 机器类型
            data['buydate'] = bsObj.find("span",
                                         {"id": "C19_W69_V72_V74_btadminh_ext.zzfld00002y"}).text.strip()  # 购买日期
            data['ordername'] = bsObj.find("span", {"id": "C19_W69_V72_V74_thtmlb_textView_20"}).text.strip()  # 增值服务项

        data['description'] = self.getTableRow(bsObj,
                                               "C23_W83_V84_V85_TextList_TableHeader" if not statuscode else "C24_W90_V91_V92_TextList_TableHeader",
                                               lambda row: self.findspan(row[0]) + ":" + self.finda(row[1]) + "\n")
        yield self.userdetail(data, url, params, statuscode)

    def getFinishTime(self, data, url, params):
        # print('=========================getFinishTime 获取工单完工时间')
        param = {"callbackFlashIslands": params["callbackFlashIslands"],
                 "callbackSilverlightIslands": params["callbackSilverlightIslands"],
                 "wcf-secure-id": params["wcf-secure-id"], "LTX_PREFIX_ID": params["LTX_PREFIX_ID"],
                 "PREFIX_ID": 'C9_W36_V37_', "crmFrwScrollXPos": '0', "crmFrwOldScrollXPos": '0',
                 "currentDate": params["currentDate"], 'htmlbevt_ty': "thtmlb:tableView:navigate:null",
                 'htmlbevt_oid': "C31_W114_V115_DatesTable", 'htmlbevt_frm': "myFormId", 'htmlbevt_id': "tvNavigator",
                 'htmlbevt_cnt': "1", 'htmlbevt_par1': "page:2,11,10,18,P",
                 'sap-ajaxtarget': "C1_W1_V2_C1_W1_V2_V3_C19_W69_V72_C31_W114_V115_Dates.do",
                 'sap-ajax_dh_mode': "AUTO", 'onInputProcessing': "htmlb", 'C13_W47_V48_SearchMenuAnchor1': "UP",
                 'C8_W34_V35_RecentObjects_isExpanded': "yes", 'C23_W85_V86_V88_Table_editMode': "NONE",
                 'C19_W69_V72_0001_displaymode': "X", 'C23_W85_V86_V87_itemobjecttype_itemobjecttype': "ALL",
                 'C23_W85_V86_V88_Table_isCellerator': "TRUE", 'C23_W85_V86_V88_Table_rowCount': "1",
                 'C23_W85_V86_V88_Table_visibleFirstRow': "1",
                 'C23_W85_V86_V88_Table_bindingString': "//BTAdminI/Table",
                 'C23_W85_V86_V88_Table_isNavModeActivated': "TRUE",
                 'C23_W85_V86_V88_Table_configHash': "9EEC78D4306657883F5C86BEFC0745B37DA819FE",
                 'C23_W85_V86_V88_Table_multiParameter': "0////0////0////0", 'C19_W69_V72_0002_displaymode': "X",
                 'C24_W90_V91_V92_TextList_rowCount': "3", 'C24_W90_V91_V92_TextList_visibleFirstRow': "1",
                 'C24_W90_V91_V92_TextList_bindingString': "//Text/Table",
                 'C24_W90_V91_V92_TextList_isNavModeActivated': "TRUE",
                 'C24_W90_V91_V92_TextList_configHash': "0E513D2C7268EC204F42B18C06AFE9CDEC0335E5",
                 'C24_W90_V91_V92_TextList_multiParameter': "0////0////0////0", 'C19_W69_V72_0003_displaymode': "X",
                 'C25_W94_V95_Table_isCellerator': "TRUE", 'C25_W94_V95_Table_rowCount': "0",
                 'C25_W94_V95_Table_visibleFirstRow': "1", 'C25_W94_V95_Table_bindingString': "//DocList/Table",
                 'C25_W94_V95_Table_isFrontendSelection': "TRUE", 'C25_W94_V95_Table_isNavModeActivated': "TRUE",
                 'C25_W94_V95_Table_configHash': "2B1898492BCC377ECF844081E0C8B91EEB805379",
                 'C25_W94_V95_Table_multiParameter': "0////0////0////0", 'C19_W69_V72_0004_displaymode': "X",
                 'C19_W69_V72_0006_displaymode': "X", 'C27_W103_V104_ConfCellTable_isCellerator': "TRUE",
                 'C27_W103_V104_ConfCellTable_rowCount': "0", 'C27_W103_V104_ConfCellTable_visibleFirstRow': "1",
                 'C27_W103_V104_ConfCellTable_bindingString': "//TranceList/Table",
                 'C27_W103_V104_ConfCellTable_isNavModeActivated': "TRUE",
                 'C27_W103_V104_ConfCellTable_configHash': "7D633AD0A8F7098E6A03D3F0BBA3020EB7F11686",
                 'C27_W103_V104_ConfCellTable_multiParameter': "0////0////0////0", 'C19_W69_V72_0007_displaymode': "X",
                 'C19_W69_V72_0008_displaymode': "X", 'C29_W108_V109_ConfCellTable_isCellerator': "TRUE",
                 'C29_W108_V109_ConfCellTable_rowCount': "0", 'C29_W108_V109_ConfCellTable_visibleFirstRow': "1",
                 'C29_W108_V109_ConfCellTable_bindingString': "//ZCall/Table",
                 'C29_W108_V109_ConfCellTable_isNavModeActivated': "TRUE",
                 'C29_W108_V109_ConfCellTable_configHash': "E24612518975848E7FAA1EF476EBF26F7D025301",
                 'C29_W108_V109_ConfCellTable_multiParameter': "0////0////0////0", 'C19_W69_V72_0009_displaymode': "X",
                 'C30_W110_V111_TABLE_rowCount': "0", 'C30_W110_V111_TABLE_visibleFirstRow': "1",
                 'C30_W110_V111_TABLE_bindingString': "//ZTAB00011F/Table",
                 'C30_W110_V111_TABLE_isFrontendSelection': "TRUE", 'C30_W110_V111_TABLE_isNavModeActivated': "TRUE",
                 'C30_W110_V111_TABLE_configHash': "47B16290F9622C8097E999109F42C028F547915D",
                 'C30_W110_V111_TABLE_multiParameter': "0////0////0////0", 'C19_W69_V72_0010_displaymode': "X",
                 'C31_W114_V115_DatesTable_isCellerator': "TRUE", 'C31_W114_V115_DatesTable_rowCount': "18",
                 'C31_W114_V115_DatesTable_visibleFirstRow': "11",
                 'C31_W114_V115_DatesTable_bindingString': "//BTDate/Table",
                 'C31_W114_V115_DatesTable_isNavModeActivated': "TRUE",
                 'C31_W114_V115_DatesTable_configHash': "F1047D2E37AE2DE80BA46A1E06588EDC4440CA8A",
                 'C31_W114_V115_DatesTable_multiParameter': "0////0////0////0", 'C19_W69_V72_0011_displaymode': "X",
                 'thtmlbOverviewControllerID': "C19_W69_V72", 'crmFrwScrollYPos': "891", 'crmFrwOldScrollYPos': "891",
                 'thtmlbKeyboardFocusId': "C31_W114_V115_DatesTable_pag_pg-1", 'sap-ajax_request': "X"}
        url = url + "?sap-client=800&sap-language=ZH&sap-domainrelax=min&saprole=ZIC_AGENT_08&sapouid=50000265&sapoutype=S"
        # print("self.headers=", self.headers, ",url=", url)
        userRes = self.session.post(url, data=param, headers=self.headers)
        # print("param=", param)
        # print("getFinishTime result:", userRes.text)
        bsObj = self.getsoup(userRes)
        try:
            data['repairtime'] = self.getTableRow(bsObj, "C31_W114_V115_DatesTable_TableHeader",
                                                  lambda r: self.findspan(r[1]).replace(".", '-') + " " + self.findspan(
                                                      r[2]), row_no=-4, truncate=False)  # crm完工日期作为安装日期
        except Exception as e:
            print("getFinishTime exception", e)
        return data

    def userdetail2(self, data, url, params):
        # print('=========================userdetail2 从工单详情进入 查看用户详情')
        data['pid'] = 'C24_W88_V89_btpartner_table[1].thtmlb_oca.EDIT'  # 通过元素获取？
        oid = data['oid']
        pid = data['pid']
        del data['pid']
        del data['oid']
        param = params.copy()
        param['htmlbevt_ty'] = "thtmlb:image:click:null::CL_THTMLB_TABLE_VIEW::EDIT.1"
        param['htmlbevt_oid'] = pid
        param['thtmlbKeyboardFocusId'] = pid
        param['htmlbevt_id'] = "ONE_CLICK_ACTION"
        param['htmlbevt_cnt'] = "0"
        param['sap-ajaxtarget'] = "C1_W1_V2_C1_W1_V2_V3_C24_W84_V87_C29_W103_V104_Partner.do"
        param['C23_W85_V86_V88_Table_configHash'] = "9EEC78D4306657883F5C86BEFC0745B37DA819FE"
        param['C24_W90_V91_V92_TextList_configHash'] = "0E513D2C7268EC204F42B18C06AFE9CDEC0335E5"
        param['C24_W90_V91_V92_TextList_multiParameter'] = "0////0////0////0"
        param['C24_W90_V91_V92_TextList_bindingString'] = "//Text/Table"
        userRes = self.session.post(url, data=param, headers=self.headers)
        bsObj = self.getsoup(userRes)
        data['mobile'] = str(bsObj.find("input", {"id": "C30_W123_V124_commdata_telephonetel"})["value"])
        data['province'] = str(bsObj.find("input", {"id": "C30_W119_V120_postaldata_region_text"})["value"])
        data['city'] = str(bsObj.find("input", {"id": "C30_W119_V120_postaldata_city"})["value"])
        data['county'] = str(bsObj.find("input", {"id": "C30_W119_V120_postaldata_district"})["value"])
        data['address'] = str(bsObj.find("input", {"id": "C30_W119_V120_postaldata_street"})["value"])  # 用户详细地址
        data = self.clearAddress(data)
        # print('=========================orderdetail2 最终数据')
        # print(data)
        self.back2order(pid, url, params)
        self.back2orderlist(oid, url, params)
        return data

    def filterstr(self, address, filterstr):
        if address and filterstr and filterstr in address and address.startswith(filterstr):
            return address.replace(filterstr, '', 1)
        else:
            return address

    def userdetail(self, data, url, params, statuscode):
        # print('=========================userdetail 从工单列表进入查看用户详情')
        oid = data['oid']
        self.back2orderlist(oid, url, params)  # 返回到工单列表
        del data['oid']
        pid = data['pid']
        del data['pid']
        params['htmlbevt_ty'] = "thtmlb:link:click:0"
        params['htmlbevt_oid'] = pid
        params['thtmlbKeyboardFocusId'] = pid
        params['htmlbevt_id'] = "SOLD_TO_PARTY"
        params['htmlbevt_cnt'] = "0"
        params['sap-ajaxtarget'] = "C1_W1_V2_C1_W1_V2_V3_C17_W61_V62_C17_W61_V62_V64_advancedsrl.do"
        params['C17_W61_V62_V64_ResultTable_configHash'] = "F698293684A5C954932EE6CB006466A1645E5EF5"
        userRes = self.session.post(url, data=params, headers=self.headers)
        bsObj = self.getsoup(userRes)  # C30_W119_V120_postaldata_street
        data['mobile'] = bsObj.find('span', id=re.compile('.TELEPHONE')).text.strip()  # 用户电话
        data['city'] = bsObj.find('input', id=re.compile('.city'))["value"]  # 用户城市
        data['address'] = str(bsObj.find('input', id=re.compile('.street'))["value"])  # 用户详细地址
        data = self.clearAddress(data)
        # print('=========================orderdetail 最终数据')
        # print(data)
        self.back2orderlist(pid, url, params)
        return data

    def back2order(self, id, url, params):
        # print('=========================后退到工单详情')
        params_new = params.copy()
        params_new['htmlbevt_ty'] = "htmlb:button:click:0"
        params_new['htmlbevt_oid'] = "C24_W111_V112_V113_thtmlb_button_1"
        params_new['thtmlbKeyboardFocusId'] = "C24_W111_V112_V113_thtmlb_button_1"
        params_new['htmlbevt_id'] = "done"
        params_new['htmlbevt_cnt'] = "0"
        params_new['sap-ajaxtarget'] = "C1_W1_V2_C1_W1_V2_V3_C24_W111_V112_C24_W111_V112_V113_PartnerEFHeader.do"
        params_new['sap-ajax_dh_mode'] = "AUTO"
        params_new['C13_W47_V48_SearchMenuAnchor1'] = "UP"
        params_new['C8_W34_V35_RecentObjects_isExpanded'] = "yes"
        self.session.post(url, data=params_new, headers=self.headers)

    def back2orderlist(self, id, url, params):
        # print('=========================返回工单列表')
        params_new = params
        params_new['htmlbevt_ty'] = "htmlb:link:click:null"
        params_new['htmlbevt_oid'] = "C1_W1_V2_V3_V55_back"
        params_new['thtmlbKeyboardFocusId'] = id
        params_new['htmlbevt_id'] = "back"
        params_new['htmlbevt_cnt'] = "1"
        params_new['htmlbevt_par1'] = "#"
        params_new['C23_W83_V84_V85_TextList_bindingString'] = "//Text/Table"
        params_new['C24_W88_V89_Table_selectedRows'] = "1"
        params_new['C24_W88_V89_Table_rowCount'] = "1"
        params_new['thtmlbOverviewControllerID'] = "C19_W69_V72"
        params_new['C28_W104_V105_Table_bindingString'] = "//DocList/Table"
        params_new['C28_W104_V105_Table_configHash'] = "2B1898492BCC377ECF844081E0C8B91EEB805379"
        params_new['C28_W104_V105_Table_multiParameter'] = "0////0////0////0"
        params_new['C19_W69_V72_0006_displaymode'] = "X"
        params_new['C27_W101_V102_ConfCellTable_multiParameter'] = "7D633AD0A8F7098E6A03D3F0BBA3020EB7F11686"
        params_new['C27_W101_V102_ConfCellTable_configHash'] = "0////0////0////0"
        params_new['C24_W88_V89_Table_allRowSelected'] = "FALSE"
        params_new['C25_W92_V93_V95_Table_bindingString'] = "//BTAdminI/Table"
        params_new['sap-ajaxtarget'] = "C1_W1_V2_C1_W1_V2_V3_C1_W1_V2_V3_V55_BreadCrumbView.do"
        self.session.post(url, data=params_new, headers=self.headers)


if __name__ == '__main__':
    hdscrap = HDScrap('01007544', pwd='160324', adminid='24', bjdomain='http://gsn.bangjia.me')
    res = hdscrap.loginHd()
    # grap_res = hdscrap.transfer_order()
    # print(grap_res)
    grap_res = hdscrap.transfer_order(statuscode='M0010ZSIC0003')
    print(grap_res)
    # grap_res = hdscrap.transfer_order(statuscode='M0013ZSIC0004')
    # print(grap_res)
