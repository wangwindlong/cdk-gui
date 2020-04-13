import os
import sys
import time
from datetime import datetime
from datetime import timedelta

import wx
import wx.adv
import wx.lib.mixins.inspection
import wx.lib.mixins.listctrl as listmix
import searchutil

AppTitle = "报表管理"
VERSION = 0.1


class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        super(MyListCtrl, self).__init__(parent, id, pos, size, style)

        # ------------

        listmix.ListCtrlAutoWidthMixin.__init__(self)

        # ------------

        # Simplified init method.
        self.CreateColumns()
        self.SetProperties()

    # ---------------------------------------------------------------------------

    def CreateColumns(self):
        """
        Create columns for listCtrl.
        """
        self.InsertColumn(col=0, heading="ID", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=1, heading="操作人", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=2, heading="建单量", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=3, heading="派单量", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=4, heading="完工审核量", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=5, heading="工资结算量", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=6, heading="回访量", format=wx.LIST_FORMAT_LEFT)

        # ------------

        # ASTUCE (Tip) - ListCtrlAutoWidthMixin :
        # pour diminuer le scintillement des colonnes
        # lors du redimensionnement de la mainframe,
        # regler la derniere colonne sur une largeur elevee.
        # Vous devez toujours visualiser l'ascenseur horizontal.

        # Set the width of the columns (x4).
        # Integer, wx.LIST_AUTOSIZE or wx.LIST_AUTOSIZE_USEHEADER.
        self.SetColumnWidth(col=0, width=50)
        self.SetColumnWidth(col=1, width=100)
        self.SetColumnWidth(col=2, width=60)
        self.SetColumnWidth(col=3, width=60)
        self.SetColumnWidth(col=4, width=110)
        self.SetColumnWidth(col=5, width=110)
        self.SetColumnWidth(col=6, width=60)

    def SetProperties(self):
        """
        Set the list control properties (icon, font, size...).
        """

        # Font size and style for listCtrl.
        fontSize = self.GetFont().GetPointSize()

        # Text attributes for columns title.
        # wx.Font(pointSize, family, style, weight, underline, faceName)
        if wx.Platform in ["__WXMAC__", "__WXGTK__"]:
            boldFont = wx.Font(fontSize - 1,
                               wx.DEFAULT,
                               wx.NORMAL,
                               wx.NORMAL,
                               False, "")
            self.SetForegroundColour("black")
            self.SetBackgroundColour("#ece9d8")  # ecf3fd

        else:
            boldFont = wx.Font(fontSize,
                               wx.DEFAULT,
                               wx.NORMAL,
                               wx.BOLD,
                               False, "")
            self.SetForegroundColour("#808080")
            self.SetBackgroundColour("#ece9d8")  # ecf3fd

        self.SetFont(boldFont)


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title,
                 style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_CHILDREN):
        super(MyFrame, self).__init__(parent=None, id=-1, title=title, style=style)

        # Returns application name.
        self.app_name = wx.GetApp().GetAppName()
        # Returns bitmaps folder.
        self.bitmaps_dir = wx.GetApp().GetBitmapsDir()
        # Returns icons folder.
        self.icons_dir = wx.GetApp().GetIconsDir()

        # Simplified init method.
        self.getAdminids()  # 获取所有的网点
        self.getMasters(0)  # 获取网点下的所有师傅
        self.SetProperties()  # 设置界面的属性
        self.MakeMenuBar()
        self.MakeStatusBar()
        self.CreateCtrls()
        self.BindEvents()
        self.DoLayout()

        self.OnTimer(None)

        self.timer = wx.Timer(self)
        self.timer.Start(3000)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

    def getAdminids(self):
        pass

    def getMasters(self, adminid):
        pass

    def SetProperties(self):
        """
        Set the frame properties (title, icon, size...).
        """
        # Setting some frame properties.
        frameIcon = wx.Icon(os.path.join(self.icons_dir, "icon_wxWidgets.ico"), type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(frameIcon)
        # Frame cursor.
        cursorHand = wx.Cursor(os.path.join(self.icons_dir, "hand.cur"), type=wx.BITMAP_TYPE_CUR)
        self.SetCursor(cursorHand)
        self.SetTitle("%s V%.1f" % (self.app_name, VERSION))

    def MakeMenuBar(self):
        # Set an icon to the exit/about menu item.
        emptyImg = wx.Bitmap(os.path.join(self.bitmaps_dir, "item_empty.png"), type=wx.BITMAP_TYPE_PNG)
        exitImg = wx.Bitmap(os.path.join(self.bitmaps_dir, "item_exit.png"), type=wx.BITMAP_TYPE_PNG)
        helpImg = wx.Bitmap(os.path.join(self.bitmaps_dir, "item_about.png"), type=wx.BITMAP_TYPE_PNG)

        # menu.
        mnuFile = wx.Menu()
        mnuInfo = wx.Menu()

        # mnuFile.
        # Show how to put an icon in the menu item.
        menuItem1 = wx.MenuItem(mnuFile, -1, "布局查看\tCtrl+Alt+I", "布局查看工具 !")
        menuItem1.SetBitmap(emptyImg)
        mnuFile.Append(menuItem1)
        self.Bind(wx.EVT_MENU, self.OnOpenWidgetInspector, menuItem1)

        # Show how to put an icon in the menu item.
        menuItem2 = wx.MenuItem(mnuFile, wx.ID_EXIT, "退出\tCtrl+Q", "关闭 !")
        menuItem2.SetBitmap(exitImg)
        mnuFile.Append(menuItem2)
        self.Bind(wx.EVT_MENU, self.OnExit, menuItem2)

        # mnuInfo.
        # Show how to put an icon in the menu item.
        menuItem2 = wx.MenuItem(mnuInfo, wx.ID_ABOUT, "关于\tCtrl+A", "关于软件 !")
        menuItem2.SetBitmap(helpImg)
        mnuInfo.Append(menuItem2)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuItem2)

        # menuBar.
        menubar = wx.MenuBar()

        # Add menu voices.
        menubar.Append(mnuFile, "文件")
        menubar.Append(mnuInfo, "关于")

        self.SetMenuBar(menubar)

    def MakeStatusBar(self):
        """
        Create the status bar for my frame.
        """

        # Statusbar.
        self.myStatusBar = self.CreateStatusBar(1)
        self.myStatusBar.SetFieldsCount(2)
        self.myStatusBar.SetStatusWidths([-8, -4])
        self.myStatusBar.SetStatusText("", 0)
        self.myStatusBar.SetStatusText("bangjia.me.", 1)

    def getTodayDate(self, _date, _type):
        now = _date
        print(type(now))
        zero_date = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                    microseconds=now.microsecond)
        if _type == 0:
            return zero_date
        else:
            return zero_date + timedelta(hours=23, minutes=59, seconds=59)

    def CreateCtrls(self):
        """
        Create some controls for my frame.
        """

        # Font style for wx.StaticText.
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)

        self.adminid = None
        self.masters = None
        self.userids = []
        self.startdate = self.getTodayDate(datetime.now(), 0)
        self.enddate = self.getTodayDate(datetime.now(), 1)
        # Widgets.
        self.panel = wx.Panel(self)

        # self.stEmployees = wx.StaticText(self.panel, -1, "Employees list :")
        # self.stEmployees.SetForegroundColour("gray")
        # self.stEmployees.SetFont(font)

        # Image list.
        self.il = wx.ImageList(16, 16, True)

        # Set an icon for the first column.
        self.bmp = wx.Bitmap(os.path.join(self.bitmaps_dir, "employee.png"), type=wx.BITMAP_TYPE_PNG)

        # Add image to list.
        self.img_idx = self.il.Add(self.bmp)

        self.listCtrl = MyListCtrl(self.panel, -1,
                                   style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES | wx.BORDER_SUNKEN)

        # Assign the image list to it.
        self.listCtrl.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        # Retrieve data from the database.
        # self.employeeData = self.OnLoadData()
        #
        # # Populate the wx.ListCtrl.
        # for i in self.employeeData:
        #     index = self.listCtrl.InsertItem(self.listCtrl.GetItemCount(),
        #                                      ((str(i[0]))))
        #     self.listCtrl.SetItem(index, 1, i[1])
        #     self.listCtrl.SetItem(index, 2, i[2])
        #     self.listCtrl.SetItem(index, 3, i[3])
        #     self.listCtrl.SetItem(index, 4, i[4])
        #     self.listCtrl.SetItemImage(self.listCtrl.GetItemCount() - 1,
        #                                self.img_idx)
        #
        #     # Alternate the row colors of a ListCtrl.
        #     # Mike Driscoll... thank you !
        #     if index % 2:
        #         self.listCtrl.SetItemBackgroundColour(index, "#ffffff")
        #     else:
        #         self.listCtrl.SetItemBackgroundColour(index, "#ece9d8")  # ecf3fd

        self.stSearch = wx.StaticText(self.panel, -1, 'Search "Surname" :')
        self.txSearch = wx.TextCtrl(self.panel, -1, "", size=(100, -1))
        self.txSearch.SetToolTip("Search employee !")

        self.StaticSizer = wx.StaticBox(self.panel, -1, "Commands :")
        self.StaticSizer.SetForegroundColour("red")
        self.StaticSizer.SetFont(font)

        self.bntSearch = wx.Button(self.panel, -1, "搜索")
        self.bntSearch.SetToolTip("搜索角色的操作单量 !")

        self.bntClear = wx.Button(self.panel, -1, "&Clear")
        self.bntClear.SetToolTip("Clear the search text !")

        self.bntShowAll = wx.Button(self.panel, -1, "&All")
        self.bntShowAll.SetToolTip("Show all !")

        self.bntNew = wx.Button(self.panel, -1, "&Insert")
        self.bntNew.SetToolTip("Insert a new employee !")

        self.bntEdit = wx.Button(self.panel, -1, "&Update")
        self.bntEdit.SetToolTip("Update selected employee !")

        self.bntDelete = wx.Button(self.panel, -1, "&Delete")
        self.bntDelete.SetToolTip("Delete selected employee !")

        self.bntClose = wx.Button(self.panel, -1, "&Quit")
        self.bntClose.SetToolTip("Close !")

        # 创建操作区元素
        self.wangdian_text = wx.StaticText(self.panel, -1, "选择网点:")
        self.master_text = wx.StaticText(self.panel, -1, "选择操作人:")
        self.time_text = wx.StaticText(self.panel, -1, "操作时间：")
        self.to_text = wx.StaticText(self.panel, -1, "到")
        # ch1 = wx.ComboBox(self.panel, -1, value='C', choices=searchutil.getAdminids(), style=wx.CB_SORT)
        self.ch_adminid = wx.Choice(self.panel, -1, choices=searchutil.getAdminids())
        self.ch_master = wx.Choice(self.panel, -1, choices=['全部'])
        self.start = wx.adv.DatePickerCtrl(self.panel, -1, size=(120, 22),
                                           style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.end = wx.adv.DatePickerCtrl(self.panel, -1, size=(120, 22),
                                         style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.ch_adminid.SetSelection(0)
        self.adminid = 24
        self.getAllMasters()

    def BindEvents(self):
        """
        添加事件处理
        """

        # self.txSearch.Bind(wx.EVT_TEXT, self.OnUpperCaseText)
        #
        # # Intercept the click on the wx.ListCtrl.
        # self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.listCtrl)
        # self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.listCtrl)
        # self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.listCtrl)
        #
        self.Bind(wx.EVT_BUTTON, self.OnSearch, self.bntSearch)
        # self.Bind(wx.EVT_BUTTON, self.OnClear, self.bntClear)
        # self.Bind(wx.EVT_BUTTON, self.OnShowAll, self.bntShowAll)
        # self.Bind(wx.EVT_BUTTON, self.OnNew, self.bntNew)
        # self.Bind(wx.EVT_BUTTON, self.OnEdit, self.bntEdit)
        # self.Bind(wx.EVT_BUTTON, self.OnDelete, self.bntDelete)
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.bntClose)

        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Bind(wx.EVT_CHOICE, self.on_choice_a, self.ch_adminid)
        self.Bind(wx.EVT_CHOICE, self.on_choice_m, self.ch_master)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChanged, self.start)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChanged2, self.end)

    def DoLayout(self):
        # Sizer.
        actionSizer = wx.BoxSizer(wx.HORIZONTAL)
        textSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.StaticBoxSizer(self.StaticSizer, wx.VERTICAL)

        # Assign widgets to sizers.
        # actionSizer
        # actionSizer.Add(self.stEmployees, 0, wx.BOTTOM, 5)
        actionSizer.Add(self.wangdian_text, 0, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        actionSizer.Add(self.ch_adminid, 0, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        actionSizer.Add(self.master_text, 0, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        actionSizer.Add(self.ch_master, 0, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        actionSizer.Add(self.time_text, 0, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        actionSizer.Add(self.start, 0, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE)
        actionSizer.Add(self.to_text, 0, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        actionSizer.Add(self.end, 0, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE)
        actionSizer.Add(self.bntSearch, 0, wx.ALL, border=5)
        # textSizer.
        textSizer.Add(actionSizer, 0, wx.BOTTOM, 10)
        textSizer.Add(self.listCtrl, 1, wx.EXPAND)

        # btnSizer.
        btnSizer.Add(self.stSearch)
        btnSizer.Add(self.txSearch)
        # btnSizer.Add((5, 5), -1)
        # btnSizer.Add(self.bntSearch, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.bntClear, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.bntShowAll, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.bntNew, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.bntEdit, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.bntDelete, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.bntClose, 0, wx.ALL, 5)

        # Assign to mainSizer the other sizers.
        mainSizer.Add(textSizer, 1, wx.ALL | wx.EXPAND, 10)
        mainSizer.Add(btnSizer, 0, wx.ALL, 10)
        mainSizer.Hide(btnSizer)

        # Assign to panel the mainSizer.
        self.panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        # mainSizer.SetSizeHints(self)

    def OnOpenWidgetInspector(self, event):
        """
        Activate the widget inspection tool,
        giving it a widget to preselect in the tree.
        Use either the one under the cursor,
        if any, or this frame.
        """

        from wx.lib.inspection import InspectionTool
        wnd = wx.FindWindowAtPointer()
        if not wnd:
            wnd = self
        InspectionTool().Show(wnd, True)

    def on_combobox(self, event):
        print("选择{0}".format(event.GetString()))

    def on_choice_a(self, event):
        self.adminid = event.GetString()
        print("选择网点id:{}".format(self.adminid))
        self.ch_master.Clear()
        self.getAllMasters()

    def getAllMasters(self):
        self.masters = searchutil.getMasters(self.adminid)
        # masterStr = []
        # self.ch_master.Client(0, None)
        for index, master in enumerate(self.masters):
            if index != 0:
                self.userids.append(str(master['userid']))
            # masterStr.append(str(master['username']))
            self.ch_master.Append(master['username'], master)
        # self.ch_master.SetItems(masterStr)  # 可行
        self.ch_master.SetSelection(0)

    def on_choice_m(self, event):
        print("选择操作人:{}".format(event.GetString()))
        print("选择到操作人的其他参数:{}".format(event.GetClientData()))

    def OnDateChanged(self, evt):
        print("OnDateChanged: %s\n" % evt.GetDate())
        # self.log.write("OnDateChanged: %s\n" % evt.GetDate())
        self.startdate = self.getTodayDate(wx.wxdate2pydate(evt.GetDate()), 0)
        print("OnDateChanged2 startdate: %s\n" % self.startdate)
        pass

    def OnDateChanged2(self, evt):
        print("OnDateChanged2: %s\n" % evt.GetDate())
        # self.log.write("OnDateChanged2: %s\n" % evt.GetDate())
        self.enddate = self.getTodayDate(wx.wxdate2pydate(evt.GetDate()), 1)
        print("OnDateChanged2 enddate: %s\n" % self.enddate)
        pass

    def OnSearch(self, event):
        print("OnSearch")
        # print(self.ch_adminid.GetSelection())  # 选中的索引
        # itemObject = self.ch_adminid.GetClientData(self.ch_adminid.GetSelection())
        if self.ch_master.GetSelection() == 0:
            # userid = self.ch_master.GetItems()  # 获取到了所有的展示名称列表
            userid = self.userids
        else:
            userid = self.ch_master.GetClientData(self.ch_master.GetSelection())
        print("adminid={}, userid={}".format(self.adminid, userid))
        print("startdate={}, enddate={}".format(self.startdate, self.enddate))
        self.updateList(searchutil.getOperators(self.adminid, userid,
                                                self.startdate.strftime('%Y-%m-%d %H:%M:%S'),
                                                self.enddate.strftime('%Y-%m-%d %H:%M:%S')))
        pass

    def updateList(self, datas):
        self.listCtrl.SetFocus()
        self.listCtrl.DeleteAllItems()
        print(datas)
        # Populate the wx.ListCtrl.
        for _index, _data in enumerate(datas):
            index = self.listCtrl.InsertItem(self.listCtrl.GetItemCount(),str(_index + 1))
            if not _data['datas']:
                print()
            for items in _data['datas']:
                print(items)

                data = {}
                username = ''
                # 操作类别：1:建单 2:派单 3:审核 4:结算 5:回访
                for item in items:
                    username = item['username']
                    data[str(item['opertype'])] = item['total_count']

            self.listCtrl.SetItem(index, 1, username)
            self.listCtrl.SetItem(index, 2, 0 if '1' not in data else data['1'])
            self.listCtrl.SetItem(index, 3, 0 if '2' not in data else data['2'])
            self.listCtrl.SetItem(index, 4, 0 if '3' not in data else data['3'])
            self.listCtrl.SetItem(index, 5, 0 if '4' not in data else data['4'])
            self.listCtrl.SetItem(index, 6, 0 if '5' not in data else data['5'])
            self.listCtrl.SetItemImage(self.listCtrl.GetItemCount() - 1, self.img_idx)

            # Alternate the row colors of a ListCtrl.
            # Mike Driscoll... thank you !
            if index % 2:
                self.listCtrl.SetItemBackgroundColour(index, "#ffffff")
            else:
                self.listCtrl.SetItemBackgroundColour(index, "#ece9d8")  # ecf3fd

    @ staticmethod
    def OnAbout(event):
        message = """wangdian.bangjia.me\n
                     帮家报表管理系统
                     使用wxPython开发.\n
                     当前版本 : %.1f""" % VERSION

        wx.MessageBox(message,
                      AppTitle,
                      wx.OK)

    def OnClose(self):
        ret = wx.MessageBox("确定要退出吗 ?",
                            AppTitle,
                            wx.YES_NO | wx.ICON_QUESTION |
                            wx.CENTRE | wx.NO_DEFAULT)

        return ret

    def OnExit(self, event):
        # Ask for exit.
        intChoice = self.OnClose()

        if intChoice == 2:
            # Disconnect from server.
            # self.con.OnCloseDb()
            self.Destroy()

    def OnTimer(self, event):
        t = time.localtime(time.time())
        sbTime = time.strftime("当前时间 %d/%m/%Y are %H:%M:%S", t)
        self.myStatusBar.SetStatusText(sbTime, 0)


class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):

    def OnInit(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        self.SetAppName("帮家报表系统")
        self.InitInspection()
        self.installDir = os.path.split(os.path.abspath(sys.argv[0]))[0]
        self.locale = wx.Locale(wx.LANGUAGE_CHINESE_SIMPLIFIED)
        print("OnInit sys.argv[0]={}".format(sys.argv[0]))
        print("OnInit installDir={}".format(self.installDir))
        frame = MyFrame(None, -1, title="")
        frame.SetSize(800, 527)
        self.SetTopWindow(frame)
        frame.Center()
        frame.Show(True)

        return True

    def GetInstallDir(self):
        """
        Returns the installation directory for my application.
        """

        return self.installDir

    def GetIconsDir(self):
        """
        Returns the icons directory for my application.
        """

        icons_dir = os.path.join(self.installDir, "icons")
        return icons_dir

    def GetBitmapsDir(self):
        """
        Returns the bitmaps directory for my application.
        """

        bitmaps_dir = os.path.join(self.installDir, "bitmaps")
        return bitmaps_dir


def main():
    app = MyApp(redirect=False)
    app.MainLoop()


if __name__ == "__main__":
    main()
