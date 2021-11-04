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
from tkFunction import *
from wind import *
import threading


flag = True
version = '4.0.0'

root = Tk()
root.title('广轻网络助手 Ver {}'.format(version))
root.geometry('717x510')
root.resizable(0, 0)  # 防止用户调整尺寸
root.iconbitmap('favicon.ico')


info = Text(height=30, width=102, state=DISABLED, bg='black', fg='white')
configBtn = Button(height=4, width=12, text='设置',
                   command=lambda: configWindow(root, info))

exitBtn = Button(height=1, width=20, text='退出脚本', command=root.destroy)
pingBtn = Button(height=1, width=20, text="检查网络连通性",
                 command=lambda: pingBaidu(info))
linkBtn = Button(height=1, width=20, text="连接校园网",
                 command=lambda: linkNet(info))
logBtn = Button(height=1, width=20, text="导出日志文件",
                command=lambda: exportLog(info))
ipBtn = Button(height=1, width=20, text="打开IP查询页面",
               command=lambda: webbrowser.open_new("http://net.30202.co/"))
updateBtn = Button(height=1, width=20, text="广轻学校官网",
                   command=lambda: webbrowser.open_new("https://www.gdqy.edu.cn/"))
statusbar = Label(root, text="校园网助手运行ing......    ver {} 更新内容:集成了路由模式，优化使用体验\t 作者:氯磷Rolin".format(version),
                  bd=1, relief=SUNKEN, anchor=W)

config = getConfig()
list = config.sections()  # 获取到配置文件中所有分组名称

# 取不到配置文件时，先处理硬配置，优先打开子窗口
if list == []:
    config.add_section("system")
    config.set("system", "sleepTime", '12')
    config.set("system", "url", 'http://10.0.0.37:801/eportal/')
    config.set("system", "ip", get_host_ip())
    config.add_section("user")
    config.set("user", "account", "2019060703300")
    config.set("user", "password", "0000000000")
    if not os.path.exists("config"):
        os.mkdir("config")
    config.write(open("config\\config.ini", "w"))
    configWindow(root, info, type=1)
else:
    if re.match("172.", get_host_ip()):
        config.set("system", "ip", get_host_ip())
        config.write(open("config\\config.ini", "r+"))
        addText(info, "检测到你的IP为校园网IP：{},为你自动更新配置文件\n".format((get_host_ip())))
    else:
        addText(info, "您目前的IP为:{0},你很有可能连接在路由下面,将不为你更新配置文件\n当前IP:{1},如果IP地址有误，请务必修改设置\n\n".format(
            get_host_ip(), config.get("system", "ip")))


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
statusbar.bind("<Button-1>", openBilibili)


# 脚本运行线程
t1 = threading.Thread(target=scriptRun, args=(info, version, statusbar,))
if __name__ == '__main__' and flag:
    stop_threads = False
    t1.setName('script')
    t1.setDaemon(True)
    t1.start()

# 软件版本更新提示线程
# t2 = threading.Thread(target=acu, args=(version, info, root,))
# t2.setName('acu')
# t2.setDaemon(True)
# t2.start()

root.mainloop()
