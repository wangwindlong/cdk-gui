#!/usr/bin/env python
import time

import wx
import wx.adv

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        textSizer = wx.BoxSizer(wx.VERTICAL)
        # self.stEmployees = wx.StaticText(self, -1, "你好，这个是测试文本", style=wx.ALIGN_CENTER)
        # self.stEmployees.SetForegroundColour("gray")
        # self.stEmployees.SetFont(font)
        # textSizer.Add(self.stEmployees,  flag=wx.CENTER)
        title = wx.StaticText(self, -1, "This is an example of static text", style=wx.ALIGN_CENTER)
        center = wx.StaticText(self, -1, "align center", style=wx.ALIGN_CENTER)
        center.SetForegroundColour('white')
        center.SetBackgroundColour('black')
        textSizer.Add(title, 0, wx.EXPAND, 10)
        textSizer.Add(center, 0, wx.EXPAND, 10)
        self.SetSizer(textSizer)
        textSizer.Fit(self)

        import datetime

        def subtime(date1, date2):
            date1 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
            date2 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")

            return date2 - date1

        date1 = r'2015-06-19 02:38:01'
        date2 = r'2015-06-18 05:31:22'

        # print(time.gmtime())
        print(subtime(date1, date2))  # date1 > date2
        print(subtime(date2, date1))  # date1 < date2

        nowdate = datetime.datetime.now()  # 获取当前时间
        nowdate = nowdate.strftime("%Y-%m-%d %H:%M:%S")  # 当前时间转换为指定字符串格式
        print(subtime(date2, nowdate))  # nowdate > date2

        # In some cases the widget used above will be a native date
        # picker, so show the generic one too.
        # dpc = wx.adv.DatePickerCtrlGeneric(self, size=(120,-1),
                                       # style = wx.TAB_TRAVERSAL
                                       # | wx.adv.DP_DROPDOWN
                                       # | wx.adv.DP_SHOWCENTURY
                                       # | wx.adv.DP_ALLOWNONE )
        # self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
        # sizer.Add(dpc, 0, wx.LEFT, 50)


    def OnDateChanged(self, evt):
        self.log.write("OnDateChanged: %s\n" % evt.GetDate())

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.DatePickerCtrl</center></h2>

This control allows the user to select a date. Unlike
wx.calendar.CalendarCtrl, which is a relatively big control,
wx.DatePickerCtrl is implemented as a small window showing the
currently selected date. The control can be edited using the keyboard,
and can also display a popup window for more user-friendly date
selection, depending on the styles used and the platform.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

