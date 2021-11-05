'''
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-09-18 19:31:08
LastEditors: Rolin
Code-Function-What do you want to do: 
FilePath: \创新创业案例-区块链即时通讯d:\Project\vscode-workspace\python\src\LoginNetwork\release\tkLoginScript.py
'''

import webbrowser
from time import thread_time_ns
import utils
import network
import wind
import threading
import config as c
from tkinter import *
import configparser
import os


flag = True

root = Tk()
root.title('广轻网络助手 Ver {}'.format(c.VERSION))
root.geometry('717x510')
root.resizable(0, 0)  # 防止用户调整尺寸
root.iconbitmap('favicon.ico')


# 控件绘制
info = Text(height=30, width=102, state=DISABLED, bg='black', fg='white')
configBtn = Button(height=4, width=12, text='设置',
                    command=lambda: wind.configWindow(root, info))
exitBtn = Button(height=1, width=20, text='退出脚本', command=root.destroy)
pingBtn = Button(height=1, width=20, text="检查网络连通性",
                    command=lambda: utils.pingBaidu(info))
linkBtn = Button(height=1, width=20, text="连接校园网",
                    command=lambda: network.linkNet(info))
logBtn = Button(height=1, width=20, text="导出日志文件",
                    command=lambda: wind.exportLog(info))
ipBtn = Button(height=1, width=20, text="打开IP查询页面",
                    command=lambda: webbrowser.open_new(c.SELECT_URL))
updateBtn = Button(height=1, width=20, text="广轻学校官网",
                    command=lambda: webbrowser.open_new(c.OFFICIAL_WEB))
statusbar = Label(root, 
                    text="校园网助手运行ing......    ver {} 更新内容:集成了路由模式，优化使用体验\t 作者:氯磷Rolin".format(c.VERSION),
                    bd=1, relief=SUNKEN, anchor=W)

# 获取配置文件
config = utils.getConfig()
list = config.sections()  # 获取到配置文件中所有分组名称

# 取不到配置文件时，先处理硬配置，优先打开子窗口
if list == []:
    config.add_section("system")
    config.set("system", "sleepTime", '12')
    config.add_section("user")
    config.set("user", "account", "2019060703300")
    config.set("user", "password", "0000000000")
    if not os.path.exists("config"):
        os.mkdir("config")
    config.write(open("config\\config.ini", "w"))
    wind.configWindow(root, info, type=1)


# 控件位置
configBtn.place(x=600, y=400)
linkBtn.place(x=24, y=405)
pingBtn.place(x=224, y=405)
exitBtn.place(x=424, y=445)
ipBtn.place(x=24, y=445)
updateBtn.place(x=224, y=445)
logBtn.place(x=424, y=405)
statusbar.pack(side=BOTTOM, fill=X)
info.place(x=0, y=0)

# 控件绑定
statusbar.bind("<Button-1>", utils.statusBarCallback)


# 脚本运行线程
t1 = threading.Thread(target=network.scriptRun, args=(info, statusbar,))
if __name__ == '__main__' and flag:
    stop_threads = False
    t1.setName('script')
    t1.setDaemon(True)
    t1.start()

# 线程常驻
root.mainloop()
