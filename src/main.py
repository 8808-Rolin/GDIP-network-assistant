# 导入包
from pathlib import Path
from tkinter import *
from tkinter import messagebox
import threading
import webbrowser
import config as c
import network
import utils
import wind
from log import *
import requests
import re
import sys

flag = True
isFirst = False
in_school = True

# 资源引入
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
THEMES_PATH = Path("{}/{}".format(os.path.abspath('.'),"config\\themes"))


def relative_to_assets(path: str) -> Path:
    pa = THEMES_PATH / Path(path)
    if pa.exists():
        return pa
    else:
        return ASSETS_PATH / Path(path)



# 创建框体
window = Tk()
window.title('广轻网络助手 Ver {}'.format(c.VERSION))
window.geometry("960x586")
window.configure(bg="#FAFAFD")
window.iconbitmap(relative_to_assets('favicon.ico'))

# 判断当前是否校园网环境
try:
    requests.get(url=c.INDEX_LOGIN, timeout=1)
except Exception as e:
    ex = str(e)
    in_school = False
    if re.search(r'Failed to establish a new connection', ex) is not None:
        messagebox.showwarning(title="警告", message=c.OPEN_WARNING)
    elif re.search(r'timeout', ex) is not None:
        ru = messagebox.askyesno(title="错误！！！", message=c.OPEN_STOP)
        if not ru:
            sys.exit(1)

# 背景框体绘制
canvas = Canvas(window, bg="#FAFAFD", height=586, width=960, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

# 日志框绘制
entryBar_image = PhotoImage(file=relative_to_assets("entry_1.png"))
entryBar = canvas.create_image(350.0, 318.0, image=entryBar_image)
info = Text(bd=0, bg="#002038", highlightthickness=0, fg='#FFFFFF', state=DISABLED)
info.place(x=30.0, y=104.0, width=640.0, height=431.0)

# 顶部图片
topBar_image = PhotoImage(file=relative_to_assets("image_1.png"))
topBar = canvas.create_image(480.0, 32.0, image=topBar_image)

# 提示文字
canvas.create_text(45.0, 81.0, anchor="nw", text="校园网连接日志", fill="#000000", font=("Roboto", 12 * -1))

# 连接校园网
link_image = PhotoImage(file=relative_to_assets("button_1.png"))
link = Button(image=link_image, borderwidth=0, highlightthickness=0, relief="flat",
              command=lambda: network.linkNet(info))
link.place(x=700.0, y=262.0, width=240.0, height=40.0)

# 打开IP查询页面
ip_image = PhotoImage(file=relative_to_assets("button_2.png"))
ipBtn = Button(image=ip_image, borderwidth=0, highlightthickness=0, relief="flat",
               command=lambda: webbrowser.open_new(c.SELECT_URL))
ipBtn.place(x=700.0, y=321.0, width=240.0, height=40.0)

# 设置按钮
setting_image = PhotoImage(file=relative_to_assets("button_3.png"))
settingBtn = Button(image=setting_image, borderwidth=0, highlightthickness=0, relief="flat",
                    command=lambda: wind.configWindow(window, info))
settingBtn.place(x=700.0, y=500.0, width=240.0, height=40.0)

# 检查网络连通性按钮
ping_image = PhotoImage(file=relative_to_assets("button_4.png"))
pingBtn = Button(image=ping_image, borderwidth=0, highlightthickness=0, relief="flat",
                 command=lambda: utils.pingBaidu(info))
pingBtn.place(x=700.0, y=381.0, width=110.0, height=40.0)

# 打开广轻官网
web_image = PhotoImage(file=relative_to_assets("button_5.png"))
webBtn = Button(image=web_image, borderwidth=0, highlightthickness=0, relief="flat",
                command=lambda: webbrowser.open_new(c.OFFICIAL_WEB))
webBtn.place(x=830.0, y=381.0, width=110.0, height=40.0)

# 导出日志按钮
log_image = PhotoImage(file=relative_to_assets("button_6.png"))
logBtn = Button(image=log_image, borderwidth=0, highlightthickness=0, relief="flat",
                command=lambda: utils.exportLog(info))
logBtn.place(x=700.0, y=441.0, width=110.0, height=40.0)

# 退出按钮
exit_image = PhotoImage(file=relative_to_assets("button_7.png"))
exitBtn = Button(image=exit_image, borderwidth=0, highlightthickness=0, relief="flat",
                 command=window.destroy)
exitBtn.place(x=830.0, y=441.0, width=110.0, height=40.0)

# 展示图片位置
image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(820.0, 165.0, image=image_image_2)

# 底部状态栏
statusbar = Label(window,
                  text="校园网助手Ver{}初始化中...... ".format(c.VERSION),
                  bd=1, bg='yellow', relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

# ----业务代码----

# 获取配置文件
config = utils.getConfig()
list = config.sections()  # 获取到配置文件中所有分组名称

# 日志类
logger = log(info)

# 取不到配置文件时，先处理硬配置，优先打开子窗口
if not list:
    if not os.path.exists("config"):
        os.mkdir("config")
    logger.addText("首次使用，请务必打开设置填写账号密码方可使用")
    isFirst = True
else: # 存在配置文件，判断每一项是否存在，不存在则填充
    if not config.has_section("theme"):
        config.add_section("theme")

    if not config.has_section("system"):
        config.add_section('system')

    if not config.has_section("user"):
        config.add_section('user')

    if not config.has_option("user","account"):
        num = utils.get_account(info)
        if num == '':
            config.set("user", "account", "2019060703300")
        else:
            config.set("user", "account", num)

    if not config.has_option("user","password"):
        config.set("user", "password", "0000000000")

    if not config.has_option("system","sleepTime"):
        config.set("system", "sleepTime", '10')

    config.set("system", "lastUseTime",time.strftime("%Y 年 %m 月 %d 日 %H:%M:%S", time.localtime()))

    if not config.has_option("theme","日志框背景颜色"):
        config.set("theme", "日志框背景颜色", '#002038')
    if not config.has_option("theme","日志框文字颜色"):
        config.set("theme", "日志框文字颜色", '#FFFFFF')
    if not config.has_option("theme", "软件背景颜色"):
        config.set("theme", "软件背景颜色", '#FAFAFD')

config.write(open("config\\config.ini", "w",encoding='UTF-8'))

# 根据配置修改控件颜色
info['bg'] = config.get('theme','日志框背景颜色')
info['fg'] = config.get('theme','日志框文字颜色')
canvas['bg'] = config.get("theme", "软件背景颜色")

# 控件绑定
statusbar.bind("<Button-1>", utils.statusBarCallback)

# 主脚本运行线程
t1 = threading.Thread(target=network.scriptRun, args=(info, statusbar,))
t2 = threading.Thread(target=utils.usbct, args=(statusbar, info,))
if __name__ == '__main__' and flag:
        stop_threads = False
        t1.daemon = True
        t1.name = 'script'
        t1.start()

        t2.daemon = True
        t2.name = 'statusbar'
        t2.start()


# 线程常驻
window.resizable(False, False)
# 如果没有配置则打开配置选项
if isFirst:
    wind.configWindow(window, info)
    isFirst = False
window.mainloop()
