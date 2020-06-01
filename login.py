import datetime
import json
import os
import sys
import time

import wx
import wx.adv
import wx.lib.mixins.inspection
from apscheduler.triggers import interval

from CDKUtil import CDKUtil
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

AppTitle = "CDK抓单"
VERSION = 0.1


def refresh_order(frame):
    print("refresh_order frame={}".format(frame))
    success = wx.GetApp().cdkutil.loadHaierOrder()
    if not success:
        wx.GetApp().logout(frame)
    else:
        wx.GetApp().addCount()
        wx.GetApp().setLast()


class MainFrame(wx.Frame):
    def __init__(self, userinfo):
        wx.Frame.__init__(self, parent=None, title='CDK抓单中...')
        self.loginTime = wx.GetApp().GetLoginTime()
        self.userinfo = userinfo
        self.makeStatusBar()
        self.initText()

        self.OnTimer(None)

        self.timer = wx.Timer(self)
        self.timer.Start(3000)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        wx.GetApp().startJob(self)

    def initText(self):
        textSizer = wx.BoxSizer(wx.VERTICAL)
        self.main_txt = wx.StaticText(self, -1, "登录时长 %s".format(MyApp.getCurrentDateTime() - self.loginTime),
                                      style=wx.ALIGN_CENTER)
        self.count_txt = wx.StaticText(self, -1, "同步次数：{}".format(wx.GetApp().getCount()), style=wx.ALIGN_CENTER)
        self.last_txt = wx.StaticText(self, -1, "最近更新时间：{}".format(wx.GetApp().getLast()), style=wx.ALIGN_CENTER)
        # center.SetForegroundColour('white')
        # center.SetBackgroundColour('black')
        textSizer.Add(self.main_txt, 0, wx.EXPAND, 10)
        textSizer.Add(self.count_txt, 0, wx.EXPAND, 10)
        textSizer.Add(self.last_txt, 0, wx.EXPAND, 10)
        self.SetSizer(textSizer)
        textSizer.Fit(self)

    def OnTimer(self, event):
        t = MyApp.getCurrentDateTime()
        sbTime = "当前时间 {}".format(t.strftime("%Y-%m-%d %H:%M:%S"))
        self.myStatusBar.SetStatusText(sbTime, 0)
        self.main_txt.SetLabel("登录时长 {}".format(t - self.loginTime))
        self.count_txt.SetLabel("同步次数：{}".format(wx.GetApp().getCount()))
        self.last_txt.SetLabel("最近更新时间：{}".format(wx.GetApp().getLast()))
        self.Layout()

    def makeStatusBar(self):
        self.myStatusBar = self.CreateStatusBar(1)
        self.myStatusBar.SetFieldsCount(2)
        self.myStatusBar.SetStatusWidths([-8, -4])
        self.myStatusBar.SetStatusText("", 0)
        self.myStatusBar.SetStatusText("bangjia.me.", 1)


class LoginFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title=AppTitle)
        # panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        userInfo = wx.GetApp().getUserInfo()
        if userInfo and 'username' in userInfo:
            default_name = userInfo['username']
        else:
            default_name = "66004185"

        if userInfo and 'passwd' in userInfo:
            default_pwd = userInfo['passwd']
        else:
            default_pwd = "Dw147259"

        self.txt_username = wx.TextCtrl(self, value=default_name)
        self.add_widgets("账号", self.txt_username)

        self.txt_password = wx.TextCtrl(self, value=default_pwd, style=wx.TE_PASSWORD)
        self.add_widgets("密码", self.txt_password)

        self.txt_code = wx.TextCtrl(self, value="")
        # 添加验证码图片，并加入页面布局，为第三行，第3列
        # image = wx.Image(os.path.join(wx.GetApp().resource_path(''), "bitmaps",'item_empty.png'),
        #                  wx.BITMAP_TYPE_PNG).Rescale(80, 25).ConvertToBitmap()  # 获取图片，转化为Bitmap形式
        self.img_code = wx.StaticBitmap(self, -1)  # 转化为wx.StaticBitmap()形式
        self.img_code.Bind(wx.EVT_LEFT_DOWN, self.loadCodeImg)
        self.add_widgets("验证码", self.txt_code).Add(self.img_code, 0, wx.ALL, 5)

        # self.title = wx.TextCtrl(self, value="")
        # self.add_widgets("验证码", self.title)

        btn_sizer = wx.BoxSizer()
        save_btn = wx.Button(self, label="登录")
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)

        exit_btn = wx.Button(self, label="退出")
        exit_btn.Bind(wx.EVT_BUTTON, self.on_exit)
        btn_sizer.Add(save_btn, 0, wx.ALL, 5)
        btn_sizer.Add(exit_btn, 0, wx.ALL, 5)
        # btn_sizer.Add(wx.Button(self, id=wx.ID_CANCEL), 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.CENTER)

        self.SetSizer(self.main_sizer)
        self.loadCodeImg()
        self.Show()
        self.main_window = None

        self.Bind(wx.EVT_BUTTON, self.OnExit, exit_btn)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def add_widgets(self, label_text, text_ctrl):
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label=label_text, size=(50, -1))
        row_sizer.Add(label, 0, wx.ALL, 5)
        row_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(row_sizer, 0, wx.EXPAND)
        return row_sizer

    def loadCodeImg(self, event=None):
        # response = requests.get(url)
        # img = Image.open(BytesIO(response.content))
        img = wx.GetApp().cdkutil.generateCode()
        # image = wx.Image(img.size[0], img.size[1])
        image = wx.Image(img.size[0], img.size[1])
        image.SetData(img.convert("RGB").tobytes())
        self.img_code.SetBitmap(image.Rescale(80, 25).ConvertToBitmap())

    def on_save(self, event):
        print("登录")
        # 开始登录，登录成功后保存信息到本地
        username = self.txt_username.GetValue()
        passwd = self.txt_password.GetValue()
        code = self.txt_code.GetValue()
        wx.GetApp().cdkutil.username = username
        wx.GetApp().cdkutil.passwd = passwd
        success = wx.GetApp().cdkutil.checkCode(code, username, passwd)
        print("登录 success: {}".format(success))
        # todo 写入文件？
        if success:
            wx.GetApp().SetLoginTime()
            self.main_window = MainFrame(wx.GetApp().getUserInfo())
            self.main_window.SetSize(800, 527)
            self.main_window.Center()
            self.main_window.Show(True)
            self.Hide()
            self.main_window.Bind(wx.EVT_CLOSE, self.on_exit)
        else:
            wx.GetApp().cdkutil.token = ''
            userinfo = {"username": username, "passwd": passwd, "token": '', 'islogin': False, 'orderurl': ''}
            wx.GetApp().setUserInfo(userinfo)

    def on_exit(self, event):
        print("exit")
        user = wx.GetApp().getUserInfo()
        # closed_window = event.EventObject
        # if closed_window == self.main_window:
        #     self.main_window = None
        #     self.Show()
        # elif closed_window == self:
        #     print('Carry out your code for when Main window closes')
        # event.Skip()
        self.OnExit(event)

    def OnClose(self):
        ret = wx.MessageBox("确定要退出吗 ?",
                            AppTitle,
                            wx.YES_NO | wx.ICON_QUESTION |
                            wx.CENTRE | wx.NO_DEFAULT)
        return ret

    def OnExit(self, event):
        # Ask for exit.
        print("OnExit")
        print(event)
        intChoice = self.OnClose()
        print(intChoice)

        if intChoice == 2:
            # Disconnect from server.
            # self.con.OnCloseDb()
            # 结束循环任务
            wx.GetApp().stopJob()
            closed_window = event.EventObject
            if closed_window == self.main_window:
                self.main_window.Destroy()
                self.main_window = None
                # self.Show()
            # elif closed_window == self:
            #     print('Carry out your code for when Main window closes')
            # event.Skip()

            userinfo = wx.GetApp().getUserInfo()
            userinfo['islogin'] = False
            wx.GetApp().setUserInfo(userinfo)
            self.Destroy()


class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):

    def OnInit(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        self.SetAppName("CDK抓单")
        self.InitInspection()
        self.installDir = os.path.split(os.path.abspath(sys.argv[0]))[0]
        # self.installDir = self.resource_path('')
        self.locale = wx.Locale(wx.LANGUAGE_CHINESE_SIMPLIFIED)
        self.loginTime = MyApp.getCurrentDateTime()
        path = os.path.join(self.installDir, "file")
        if not os.path.exists(path):
            os.makedirs(path)
        self.userfile = os.path.join(self.installDir, "file", "user.txt")
        self.apscheduler = BackgroundScheduler()
        self.cdkutil = CDKUtil()
        self.job = None
        self.loginFrame = None
        self.mainFrame = None
        self.count = 1
        self.lasttime = self.loginTime

        print("OnInit sys.argv[0]={}".format(sys.argv[0]))
        print("OnInit installDir={}".format(self.installDir))
        userinfo = self.getUserInfo()
        frame = None
        if userinfo and 'islogin' in userinfo and 'token' in userinfo:
            if userinfo['islogin'] and userinfo['token'] and len(userinfo['token']) > 5:
                self.cdkutil.token = userinfo['token']
                self.cdkutil.username = userinfo['username']
                self.cdkutil.passwd = userinfo['passwd']
                self.cdkutil.orderurl = userinfo['orderurl']
                self.mainFrame = MainFrame(userinfo)
                frame = self.mainFrame
        if not self.mainFrame:
            self.loginFrame = LoginFrame()
            frame = self.loginFrame
        frame.SetSize(800, 527)
        self.SetTopWindow(frame)
        frame.Center()
        frame.Show(True)

        return True

    def getUserInfo(self):
        if os.path.exists(self.userfile):
            with open(self.userfile, 'r') as f:
                userinfo = json.loads(f.read())
                return userinfo
        return None

    def setUserInfo(self, userinfo):
        with open(self.userfile, 'w') as f:
            jsObj = json.dumps(userinfo)
            f.write(jsObj)

    @staticmethod
    def getCurrentDateTime():
        return datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "%Y-%m-%d %H:%M:%S")

    def SetLoginTime(self):
        self.loginTime = MyApp.getCurrentDateTime()
        # self.loginTime = time.localtime(time.time())

    def GetLoginTime(self):
        return self.loginTime

    def startJob(self, frame):
        if not self.apscheduler:
            self.apscheduler = BackgroundScheduler()
        self.apscheduler.start()
        if not self.job:
            trigger = interval.IntervalTrigger(seconds=5 * 10)
            self.job = self.apscheduler.add_job(lambda: refresh_order(frame), trigger=trigger, id='task_sync_every_5m',
                                         replace_existing=True)
            # self.job = self.apscheduler.add_job(func=refresh_order, trigger='interval', args=[frame],
            #                                     id='task_sync_every_5m', seconds=5 * 60)

    def stopJob(self):
        # self.apscheduler.shutdown(wait=False)
        if self.job:
            self.job.remove()
            self.job = None

    def logout(self, frame):
        print("logout")
        self.stopJob()
        userinfo = self.getUserInfo()
        userinfo['islogin'] = False
        self.setUserInfo(userinfo)

        wx.CallAfter(self.test, frame)

    def test(self, frame):
        print("test frame={}".format(frame))
        ret = wx.MessageBox("账号登录过期，请尝试重新登录",
                            AppTitle,
                            wx.OK | wx.ICON_INFORMATION)
        # ret = dialog.ShowModal()
        print(ret)
        if wx.OK == ret:
            print("ok pressed")
            frame.Destroy()
        # a = MyDialog(self.GetTopWindow(), "Dialog").ShowModal()
        # print(a)

    def addCount(self):
        self.count = self.count + 1

    def getCount(self):
        return self.count

    def setLast(self):
        self.lasttime = MyApp.getCurrentDateTime()

    def getLast(self):
        return self.lasttime

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


class MyDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(MyDialog, self).__init__(parent, title=title, size=(250, 150))
        panel = wx.Panel(self)
        self.btn = wx.Button(panel, wx.ID_OK, label="ok", size=(50, 20), pos=(75, 50))
        self.btn.Bind(wx.EVT_BUTTON, self.on_Ok)

    def on_Ok(self, event):
        print("MyDialog ok button clicked!!!")
        self.Close()


if __name__ == '__main__':
    app = MyApp(redirect=False)
    app.MainLoop()
