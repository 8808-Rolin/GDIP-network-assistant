
#导入包
from pathlib import Path
from tkinter import *
import os
import threading
import webbrowser
import config as c
import network
import utils
import wind
from log import *

flag = True

# 资源引入
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

# 创建框体
window = Tk()
window.title('广轻网络助手 Ver {}'.format(c.VERSION))
window.geometry("960x586")
window.configure(bg = "#FAFAFD")
window.iconbitmap(relative_to_assets('favicon.ico'))

# 背景框体绘制
canvas = Canvas(window,bg = "#FAFAFD",height = 586,width = 960,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)

# 日志框绘制
entryBar_image = PhotoImage(file=relative_to_assets("entry_1.png"))
entryBar = canvas.create_image(350.0,318.0,image=entryBar_image)
info = Text(bd=0,bg="#002038",highlightthickness=0,fg='white',state=DISABLED)
info.place(x=30.0,y=104.0,width=640.0,height=431.0)

#顶部图片
topBar_image = PhotoImage(file=relative_to_assets("image_1.png"))
topBar = canvas.create_image(480.0,32.0,image=topBar_image)

# 提示文字
canvas.create_text(45.0,81.0,anchor="nw",text="校园网连接日志",fill="#000000",font=("Roboto", 12 * -1))

# 连接校园网
link_image = PhotoImage(file=relative_to_assets("button_1.png"))
link = Button(image=link_image,borderwidth=0,highlightthickness=0,relief="flat",
        command=lambda: network.linkNet(info))
link.place(x=700.0,y=262.0,width=240.0,height=40.0)

# 打开IP查询页面
ip_image = PhotoImage(file=relative_to_assets("button_2.png"))
ipBtn = Button(image=ip_image,borderwidth=0,highlightthickness=0,relief="flat",
        command=lambda: webbrowser.open_new(c.SELECT_URL))
ipBtn.place(x=700.0,y=321.0,width=240.0,height=40.0)

# 设置按钮
setting_image = PhotoImage(file=relative_to_assets("button_3.png"))
settingBtn = Button(image=setting_image,borderwidth=0,highlightthickness=0,relief="flat",
        command=lambda: wind.configWindow(window, info))
settingBtn.place(x=700.0,y=500.0,width=240.0,height=40.0)

# 检查网络连通性按钮
ping_image = PhotoImage(file=relative_to_assets("button_4.png"))
pingBtn = Button(image=ping_image,borderwidth=0,highlightthickness=0,relief="flat",
        command=lambda: utils.pingBaidu(info))
pingBtn.place(x=700.0,y=381.0,width=110.0,height=40.0)

# 打开广轻官网
web_image = PhotoImage(file=relative_to_assets("button_5.png"))
webBtn = Button(image=web_image,borderwidth=0,highlightthickness=0,relief="flat",
        command=lambda: webbrowser.open_new(c.OFFICIAL_WEB))
webBtn.place(x=830.0,y=381.0,width=110.0,height=40.0)

# 导出日志按钮
log_image = PhotoImage(file=relative_to_assets("button_6.png"))
logBtn = Button(image=log_image,borderwidth=0,highlightthickness=0,relief="flat",
        command=lambda: utils.exportLog(info))
logBtn.place(x=700.0,y=441.0,width=110.0,height=40.0)

# 退出按钮
exit_image = PhotoImage(file=relative_to_assets("button_7.png"))
exitBtn = Button(image=exit_image,borderwidth=0,highlightthickness=0,relief="flat",
        command=window.destroy)
exitBtn.place(x=830.0,y=441.0,width=110.0,height=40.0)

# 展示图片位置
image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(820.0,165.0,image=image_image_2)

# 底部状态栏
statusbar = Label(window, 
        text="校园网助手V4运行ing......    ver {} 更新内容:新增 V2日志引擎 优化 UI交互逻辑\t如果无法获取IP请检查杀毒软件或防火墙，开启对应联网权限\t 作者:氯磷Rolin".format(c.VERSION),
        bd=1, relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

# ----业务代码----

# 获取配置文件
config = utils.getConfig()
list = config.sections()  # 获取到配置文件中所有分组名称

# 日志类
logger = log(info)

# 取不到配置文件时，先处理硬配置，优先打开子窗口
if list == []:
        config.add_section("system")
        config.set("system", "sleepTime", '12')
        config.add_section("user")
        num = utils.get_account(info)
        if(num == ''):
                config.set("user", "account", "2019060703300")
        else:
                config.set("user", "account", num)
        
        config.set("user", "password", "0000000000")
        if not os.path.exists("config"):
                os.mkdir("config")
        config.write(open("config\\config.ini", "w"))
        logger.addText("首次使用，请务必打开设置填写账号密码方可使用")



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
window.resizable(False, False)
window.mainloop()
