import requests
import json
from bs4 import BeautifulSoup
import re
from datetime import date, timedelta, datetime


class HDScrap(object):
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
        self.datasuccess = {'code': 1, 'msg': '登录成功', 'element': ''}
        self.datafail = {'code': 0, 'msg': '登录失败,请检查账号密码是否正确'}
        self.isSucess = False
        self.companyid = companyid
        self.headers = {'content-type': 'text/html', 'Accept-Encoding': 'gzip, deflate',
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
        self.headers['content-type'] = "application/x-www-form-urlencoded"
        self.headers['Referer'] = loginurl
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
            return self.continuelogon(self.session, callback)
        elif logonbtn:
            return self.datafail
        if callback:
            return callback(self.session, bsObj)
        return self.datasuccess

    def continuelogon(self, session, callback=None):
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
        self.headers['content-type'] = "application/x-www-form-urlencoded"
        url = self.baseurl + '/sap/bc/bsp/sap/crm_ui_start/default.htm'
        checkRes = session.post(url, data=params, headers=self.headers)
        # print(checkRes.status_code)
        if checkRes.status_code != 200:
            return self.datafail
        result = self.selectrole()
        if callback:
            return callback(session)
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

    def transfer_order(self):
        # print('=========================loadFrame1 加载左边的动作栏')
        url = self.baseurl + "/sap/bc/bsp/sap/crm_ui_frame/BSPWDApplication.do?sap-client=800&sap-language=ZH&sap" \
                             "-domainrelax=min&saprole=ZIC_AGENT_08&sapouid=50000265&sapoutype=S"
        self.headers['Upgrade-Insecure-Requests'] = '1'
        actionRes = self.session.get(url, headers=self.headers)
        # print(actionRes.text)
        result = self.checkstatus(actionRes)
        if result['code'] == 1:
            try:
                data = {"data": json.dumps(self.loadsearch(self.getsoup(actionRes)))}
                # print("transfer_order:")
                # print(data)
                result = requests.post(self.bjdomain + "/Api/Climborder/addorder", data=data)
                # print(result)
            except:
                return self.datafail
            return self.datasuccess
        else:
            return self.datafail

    def loadsearch(self, bsObj):
        if bsObj is None:
            return list([])
        # print('=========================loadsearch 加载工单查询初始页面')
        params = {"callbackFlashIslands": self.get_value(bsObj.find("input", {"id": "callbackFlashIslands"})),
                  "callbackSilverlightIslands": self.get_value(
                      bsObj.find("input", {"id": "callbackSilverlightIslands"})),
                  "htmlbevt_frm": "myFormId",
                  "htmlbevt_cnt": "0",
                  "onInputProcessing": "htmlb",
                  "htmlbevt_ty": "thtmlb:link:click:0",
                  "htmlbevt_id": "ZSRV-02-SR",
                  "htmlbevt_oid": "C6_W29_V30_ZSRV-01-SR",
                  "thtmlbKeyboardFocusId": "C6_W29_V30_ZSRV-01-SR",
                  "sap-ajaxtarget": "C1_W1_V2_C6_W29_V30_MainNavigationLinks.do",
                  "sap-ajax_dh_mode": "AUTO",
                  "wcf-secure-id": self.get_value(bsObj.find("input", {"id": "wcf-secure-id"})),
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
        print(url)
        self.headers['content-type'] = "application/x-www-form-urlencoded"
        self.headers['Referer'] = url
        self.headers['X-Requested-With'] = "XMLHttpRequest"
        self.headers['Accept'] = "*/*"
        roleRes = self.session.post(url, data=params, headers=self.headers)
        # print(roleRes.text)
        return list(self.search(self.getsoup(roleRes), params, 0))

    def search(self, bsObj, _params, page, totalcount=100, pagecount=10):
        # print('=========================loadsearch 搜索增值工单')
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
            'sap-ajaxtarget': target,
            'C17_W61_V62_V64_ResultTable_configHash': "0517333B2685A5CBB49408B250DF5B093056F887",
            'C17_W61_V62_V64_ResultTable_multiParameter': "0////0////0////0",
            'C17_W61_V62_V64_ResultTable_bindingString': "//BTQRSrvOrd/Table",
            'C17_W61_V62_V64_ResultTable_sortValue': 'CREATED_AT#:#desc#!#',
            'C17_W61_V62_V63_btqsrvord_max_hits': "999",
            'C17_W61_V62_thtmlbShowSearchFields': "true",
            'C17_W61_V62_V64_ResultTable_isNavModeActivated': "TRUE",
            'C17_W61_V62_V64_ResultTable_filterApplied': "FALSE", 'C17_W61_V62_V64_ResultTable_isCellerator': "TRUE",
            'C17_W61_V62_V64_ResultTable_editMode': "NONE",
            'C17_W61_V62_V64_ResultTable_visibleFirstRow': str(1 + page * 10),
            "C17_W61_V62_V63_btqsrvord_parameters[1].FIELD": "POSTING_DATE",
            "C17_W61_V62_V63_btqsrvord_parameters[1].OPERATOR": "GT",  # 时间为3天以内
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
            "C17_W61_V62_V63_btqsrvord_parameters[4].VALUE1": "01",  # 工单来源是HD-华帝
            "C17_W61_V62_V63_btqsrvord_parameters[4].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[5].FIELD": "OBJECT_ID",
            "C17_W61_V62_V63_btqsrvord_parameters[5].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[5].VALUE1": "",
            "C17_W61_V62_V63_btqsrvord_parameters[5].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[6].FIELD": "PROCESS_TYPE",
            "C17_W61_V62_V63_btqsrvord_parameters[6].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[6].VALUE1": "ZIC6",  # 工单类型为 增值服务单
            "C17_W61_V62_V63_btqsrvord_parameters[6].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[7].FIELD": "ZZFLD00003J",
            "C17_W61_V62_V63_btqsrvord_parameters[7].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[7].VALUE1": "",
            "C17_W61_V62_V63_btqsrvord_parameters[7].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[8].FIELD": "STATUS_COMMON",
            "C17_W61_V62_V63_btqsrvord_parameters[8].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[8].VALUE1": "M0002ZSIC0002",  # 状态为工单提交
            "C17_W61_V62_V63_btqsrvord_parameters[8].VALUE2": "",
            "C17_W61_V62_V63_btqsrvord_parameters[9].FIELD": "ZZFLD000062",
            "C17_W61_V62_V63_btqsrvord_parameters[9].OPERATOR": "EQ",
            "C17_W61_V62_V63_btqsrvord_parameters[9].VALUE1": "",
            "C17_W61_V62_V63_btqsrvord_parameters[9].VALUE2": "",
            'C17_W61_V62_V64_ResultTable_firstTimeRendering': "NO",
            "C9_W36_V37_POLLFREE_ALERTS": "{&#34;Alerts&#34;:[]}",
            "C17_W61_V62_V64_ResultTable_rowCount": "0" if page == 0 else str(totalcount)
        }
        if page != 0:
            params['htmlbevt_par1'] = "page:%d,%d,%d,%d,P" % (page + 1, 1 + page * pagecount, pagecount, totalcount)
        sap = re.findall(re.compile(r'[(](.*?)[)]', re.S), params['callbackFlashIslands'])[0]
        url = self.baseurl + "/sap(%s)/bc/bsp/sap/crm_ui_frame/BSPWDApplication.do" % sap
        self.headers['content-type'] = "application/x-www-form-urlencoded"
        self.headers['Referer'] = url
        roleRes = self.session.post(url, data=params, headers=self.headers)
        bsObj = self.getsoup(roleRes)
        resulttable = bsObj.find("div", {"id": "C17_W61_V62_V64_ResultTable_bottom_div"}).find("tbody")
        totalcount = int(bsObj.find("input", {"id": "C17_W61_V62_V64_ResultTable_rowCount"})["value"])
        isall = (page + 1) * pagecount >= totalcount
        print("totalcount=%d" % totalcount + ",page=%d" % page + ",isallloaded=%d" % isall)
        if resulttable:
            if isall:
                yield from self.parseorderlist(resulttable.find_all("tr"), url, params)
            else:
                yield from self.parseorderlist(resulttable.find_all("tr"), url, params)
                yield from self.search(bsObj, params, page + 1, totalcount, pagecount)

    def parseorderlist(self, trlist, url, params):
        for tr in trlist:
            tablecolumns = tr.find_all("td")
            if tr and len(tablecolumns) > 2:
                data = self.parseorder(tablecolumns)
                if data:
                    yield from self.orderdetail(self.session, data, url, params)

    def finda(self, element):
        return element.find("a").text.strip()

    def findspan(self, element):
        return element.find("span").text.strip()

    def parseorder(self, tablecolumns):
        orderno_td = tablecolumns[1]
        name_td = tablecolumns[3]
        data = {}
        orderitem = orderno_td.find("a")
        useritem = name_td.find("a")
        if orderitem and orderitem.has_attr('id'):
            data['oid'] = orderitem["id"]  # 这个是上一个列表中的工单号元素id，下一个页面需要用到
            data['pid'] = useritem['id']  # 这个是上一个列表中的用户名元素id，下一个页面需要用到
            data['factorynumber'] = self.finda(orderno_td)
            data['username'] = self.finda(name_td).split(" / ")[0]
            data['originname'] = self.findspan(tablecolumns[4])
            data['ordertime'] = self.findspan(tablecolumns[7])
            data['orderstatus'] = "工单提交"
            data['companyid'] = self.companyid
            data['machinebrand'] = "华帝"
            data['adminid'] = self.adminid
            # print(data)
            return data
        return None

    def orderdetail(self, session, data, url, params):
        # print('=========================orderdetail 查看工单详情')
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
        roleRes = session.post(url, data=params, headers=self.headers)
        bsObj = self.getsoup(roleRes)
        # print(roleRes.text)
        user_tr = bsObj.find("div", {"id": "C19_W69_V72_0003Content"}).find("tbody").find("tr")
        data['mobile'] = user_tr.find('span', id=re.compile('partner_no')).text.strip()
        data['address'] = user_tr.find('span', id=re.compile('address_short')).text.strip()
        data['repairtime'] = bsObj.find("span", {"id": "C19_W69_V72_V74_btadminh_ext.zzfld00003j"}).text.strip()  # 预约时间
        data['machinetype'] = bsObj.find("span", {"id": "C19_W69_V72_V74_thtmlb_textView_30"}).text.strip()  # 机器类型
        data['buydate'] = bsObj.find("span", {"id": "C19_W69_V72_V74_btadminh_ext.zzfld00002y"}).text.strip()  # 购买日期
        data['ordername'] = bsObj.find("span", {"id": "C19_W69_V72_V74_thtmlb_textView_20"}).text.strip()  # 增值服务项
        note_tr = bsObj.find("table", {"id": "C23_W83_V84_V85_TextList_TableHeader"}).find("tbody").find_all("tr")
        note = ""
        for note_row in note_tr:
            note_td = note_row.find_all("td")
            if note_td and len(note_td) > 2:
                note = note + self.findspan(note_td[0]) + ":" + self.finda(note_td[1]) + "\n"
        data['description'] = note
        # del data['oid']  # 清除上一个列表页面的工单元素id 不再需要，也不需要传到服务端
        data['pid'] = 'C24_W88_V89_btpartner_table[1].thtmlb_oca.EDIT'  # 通过元素获取？
        yield self.userdetail2(session, data, url, params)

    def userdetail2(self, session, data, url, params):
        # print('=========================userdetail2 从工单详情进入 查看用户详情')
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
        param['C28_W104_V105_Table_configHash'] = "2B1898492BCC377ECF844081E0C8B91EEB805379"
        param['C23_W83_V84_V85_TextList_configHash'] = "0E513D2C7268EC204F42B18C06AFE9CDEC0335E5"
        userRes = session.post(url, data=param, headers=self.headers)
        bsObj = self.getsoup(userRes)
        data['mobile'] = str(bsObj.find("input", {"id": "C30_W123_V124_commdata_telephonetel"})["value"])
        data['province'] = str(bsObj.find("input", {"id": "C30_W119_V120_postaldata_region_text"})["value"])
        data['city'] = str(bsObj.find("input", {"id": "C30_W119_V120_postaldata_city"})["value"])
        data['county'] = str(bsObj.find("input", {"id": "C30_W119_V120_postaldata_district"})["value"])
        data['address'] = str(bsObj.find("input", {"id": "C30_W119_V120_postaldata_street"})["value"])  # 用户详细地址
        # print('=========================orderdetail2 最终数据')
        # print(data)
        self.back2orderlist(session, pid, url, params)
        self.back2orderlist(session, oid, url, params)
        return data

    def userdetail(self, session, data, url, params):
        # print('=========================userdetail 从工单列表进入查看用户详情')
        oid = data['oid']
        self.back2orderlist(session, oid, url, params)  # 新的方式 不再需要回到列表
        del data['oid']
        pid = data['pid']
        params['htmlbevt_ty'] = "thtmlb:link:click:0"
        params['htmlbevt_oid'] = pid
        params['thtmlbKeyboardFocusId'] = pid
        params['htmlbevt_id'] = "SOLD_TO_PARTY"
        params['htmlbevt_cnt'] = "0"
        params['sap-ajaxtarget'] = "C1_W1_V2_C1_W1_V2_V3_C17_W61_V62_C17_W61_V62_V64_advancedsrl.do"
        params['C17_W61_V62_V64_ResultTable_configHash'] = "F698293684A5C954932EE6CB006466A1645E5EF5"
        userRes = session.post(url, data=params, headers=self.headers)
        bsObj = self.getsoup(userRes)  # C30_W119_V120_postaldata_street
        data['mobile'] = bsObj.find('span', id=re.compile('.TELEPHONE')).text.strip()  # 用户电话
        data['city'] = bsObj.find('input', id=re.compile('.city'))["value"]  # 用户城市
        data['address'] = str(bsObj.find('input', id=re.compile('.street'))["value"])  # 用户详细地址
        # print('=========================orderdetail 最终数据')
        # print(data)
        self.back2orderlist(session, pid, url, params)
        del data['pid']
        return data

    def back2orderlist(self, session, id, url, params):
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
        session.post(url, data=params_new, headers=self.headers)


if __name__ == '__main__':
    hdscrap = HDScrap('01007544', pwd='160324', adminid='24', bjdomain='http://yxgtest.bangjia.me')
    res = hdscrap.loginHd()
    grap_res = hdscrap.transfer_order()
    print(grap_res)
