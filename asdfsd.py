# 载入必要的模块
import wx
import os
import pygame
from pygame.locals import *
import itertools
import random


# 创建类
class Example(wx.Frame):
    def __init__(self, parent, title):
        # 继承父类wx.Frame的初始化方法，并设置窗口大小为320*220
        super(Example, self).__init__(parent, title=title, size=(320, 220))
        self.InitUI()
        self.Centre()
        self.Show()

    # 产生图片验证码的图像，保存在本地电脑
    def generate_picture(self):
        # pygame初始化
        pygame.init()
        # 设置字体和字号
        font = pygame.font.SysFont('consolas', 64)
        # 产生字母及数字列表，并重组，取其前四个作为图片验证码的文字
        chr_num_lst = list(itertools.chain([chr(ord('A') + _) for _ in range(26)], \
                                           [chr(ord('a') + _) for _ in range(26)], \
                                           [str(_) for _ in range(10)]))

        random.shuffle(chr_num_lst)
        self.val_text = chr_num_lst[0] + chr_num_lst[1] + chr_num_lst[2] + chr_num_lst[3]
        # 渲染图片，设置背景颜色和字体样式,前面的颜色是字体颜色
        ftext = font.render(self.val_text, True, (0, 0, 255), (255, 0, 0))
        # 保存图片
        pygame.image.save(ftext, r"%s/val.png" % os.getcwd())  # 图片保存地址

    def InitUI(self):
        # 产生验证码图片
        self.generate_picture()

        # 利用wxpython的GridBagSizer()进行页面布局
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(10, 20)  # 列间隔为10，行间隔为20

        # 添加账号字段，并加入页面布局，为第一行，第一列
        text = wx.StaticText(panel, label="账号")
        sizer.Add(text, pos=(0, 0), flag=wx.ALL, border=5)

        # 添加文本框字段，并加入页面布局，为第一行，第2,3列
        self.tc = wx.TextCtrl(panel)
        sizer.Add(self.tc, pos=(0, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        # 添加密码字段，并加入页面布局，为第二行，第一列
        text1 = wx.StaticText(panel, label="密码")
        sizer.Add(text1, pos=(1, 0), flag=wx.ALL, border=5)

        # 添加文本框字段，以星号掩盖,并加入页面布局，为第二行，第2,3列
        tc1 = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        sizer.Add(tc1, pos=(1, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        # 添加验证码字段，并加入页面布局，为第三行，第一列
        text2 = wx.StaticText(panel, label="验证码")
        sizer.Add(text2, pos=(2, 0), flag=wx.ALL, border=5)

        # 添加文本框字段，并加入页面布局，为第三行，第2列
        self.tc2 = wx.TextCtrl(panel)
        sizer.Add(self.tc2, pos=(2, 1), flag=wx.ALL, border=5)

        # 添加验证码图片，并加入页面布局，为第三行，第3列
        image = wx.Image(r'%s/val.png' % os.getcwd(),
                         wx.BITMAP_TYPE_PNG).Rescale(80, 25).ConvertToBitmap()  # 获取图片，转化为Bitmap形式
        self.bmp = wx.StaticBitmap(panel, -1, image)  # 转化为wx.StaticBitmap()形式
        sizer.Add(self.bmp, pos=(2, 2), flag=wx.ALL, border=5)

        # 添加登录按钮，并加入页面布局，为第四行，第2列
        btn = wx.Button(panel, -1, "登录")
        sizer.Add(btn, pos=(3, 1), flag=wx.ALL, border=5)

        # 为登录按钮绑定login_process事件
        self.Bind(wx.EVT_BUTTON, self.login_process, btn)
        # 将Panmel适应GridBagSizer()放置
        panel.SetSizerAndFit(sizer)

    # 事件处理
    def login_process(self, event):
        self.input_val = self.tc2.GetValue()  # 获取验证码文本框的输入文字

        # 判断验证码文本框的输入文字是否等于验证码图片上的文字（不计大小写），并弹出消息框
        if self.input_val.lower() == self.val_text.lower():
            wx.MessageBox("登录成功！\n欢迎您，%s!" % self.tc.GetValue(), '登录结果', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("登录失败！请重试！", '登录结果', wx.OK | wx.ICON_INFORMATION)
            self.tc2.SetValue("")  # 将验证码文本框清空
            self.generate_picture()  # 重新产生一张验证码图片
            # 获取新产生的验证码图片，转化为Bitmap形式
            image = wx.Image(r'%s/val.png' % os.getcwd(), wx.BITMAP_TYPE_PNG).Rescale(80, 25).ConvertToBitmap()
            # 更新GridBagSizer()的self.bmp
            self.bmp.SetBitmap(wx.BitmapFromImage(image))


# 主函数
def main():
    app = wx.App()
    Example(None, title='图片验证GUI')
    app.MainLoop()


main()
