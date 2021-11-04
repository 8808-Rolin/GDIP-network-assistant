'''
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-09-18 22:04:58
LastEditors: Rolin
Code-Function-What do you want to do: 
FilePath: \创新创业案例-区块链即时通讯d:\Project\vscode-workspace\python\src\LoginNetwork\release\wind.py
'''
from tkinter import *
from tkFunction import *
import configparser
import tkinter.messagebox  # 这个是消息框，对话框的关键
import re


def configWindow(root, text, type=0):
    # 实例化configParser对象
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read('config\\config.ini', encoding='UTF-8')

    cw = Toplevel(root)
    cw.grab_set()
    cw.geometry('300x370')
    cw.iconbitmap('favicon.ico')
    cw.title('脚本设置')
    cw.resizable(0, 0)  # 防止用户调整尺寸
    accLable = Label(master=cw, width=7, height=1, text="账号：")
    pwdLable = Label(master=cw, width=7, height=1, text="密码：")
    timeLable = Label(master=cw, width=8, height=1, text="等待时间：")
    ipLable = Label(master=cw, width=7, height=1, text="当前IP：")

    accText = Entry(master=cw, width=20)
    pwdText = Entry(master=cw, width=20)
    timeText = Entry(master=cw, width=20)
    ipText = Entry(master=cw, width=14)

    saveBtn = Button(master=cw, height=2, width=15, text='保存')
    quitBtn = Button(master=cw, height=2, width=15,
                     text='退出', command=cw.destroy)
    ipBtn = Button(cw, height=1, width=7, text="获取IP")
    autorunButton = Button(master=cw, height=1, width=15, text="添加到 开机自启")

    accLable.place(x=30, y=30)
    pwdLable.place(x=30, y=90)
    timeLable.place(x=30, y=160)
    ipLable.place(x=30, y=230)
    accText.place(x=100, y=30)
    pwdText.place(x=100, y=90)
    timeText.place(x=100, y=160)
    ipText.place(x=100, y=230)
    saveBtn.place(x=35, y=310)
    quitBtn.place(x=160, y=310)
    ipBtn.place(x=220, y=225)
    autorunButton.place(x=100, y=268)

    accText.insert(0, config.get("user", "account"))
    pwdText.insert(0, config.get('user', 'password'))
    timeText.insert(0, config.get("system", "sleepTime"))
    ipText.insert(0, config.get("system", "ip"))

    def save(elf):
        # 实例化configParser对象
        config = getConfig()

        successFlag = False
        if re.match("172.", ipText.get()):
            successFlag = True
        else:
            tkinter.messagebox.showinfo(
                "Fail", "保存设置失败！\n请检查各项参数，务必确保IP为172开头的校园网地址")

        if successFlag:
            acc = accText.get()
            pwd = pwdText.get()
            time = timeText.get()
            ip = ipText.get()

            config.set("system", "sleepTime", time)
            config.set("system", "url", 'http://10.0.0.37:801/eportal/')
            config.set("system", "ip", ip)
            config.set("user", "account", acc)
            config.set("user", "password", pwd)
            try:
                config.write(open("config\\config.ini", "r+"))
                tkinter.messagebox.showinfo("Success", "保存设置成功！")
                addText(text, "---更新设置成功---")
                addText(text, "---当前设置如下---")
                addText(text, "校园网账号：{}".format(acc))
                addText(text, "设置的IP为：{}".format(ip))
                addText(text, "等待重连的时间：{}秒".format(time))
                try:
                    # 在此处撰写同步更新IP代码
                    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
                    s = requests.session()
                    s.keep_alive = False  # 关闭多余连接
                    uri = "http://net.30202.co/update?xuehao={}&ip={}".format(
                        account, ip)
                    res = requests.get(url=uri)
                    result = json.loads(res.text)
                    if(result['status'] == 1):
                        addText(text, "同步IP成功")
                    else:
                        addText(text, "同步IP失败，请联系开发者")
                except:
                    addText(text, "同步IP出错了，等下再试把")
                cw.destroy()

            except:
                tkinter.messagebox.showinfo("Fail", "保存设置失败，请重试")

    def get_ip(ell):
        ipText.delete(0, END)
        ipText.insert(0, get_host_ip())

    saveBtn.bind("<Button-1>", save)
    ipBtn.bind("<Button-1>", get_ip)


def feedbackWindow(root, text):
    fbw = Toplevel(root)
    fbw.grab_set()
    fbw.geometry('500x300')
    fbw.title('反馈/建议')
    fbw.iconbitmap('favicon.ico')
    fbw.resizable(20, 0)  # 防止用户调整尺寸

    msgText = Text(fbw, bd=1, height=20)
    sumbit = Button(fbw, height=2, width=10, text="提交", relief=FLAT)
    msgText.insert(
        "end", '请在这里输入内容......(由于服务器限制，暂时无法传送图片与附件) 如果附上手机号码，我们将会对你的反馈进行及时回复')

    msgText.pack(side=TOP, fill=X)
    sumbit.pack(side=BOTTOM, fill=X)

    def sendMsg(self):
        config = getConfig()

        data = {
            "ip": get_host_ip(),
            "account": config.get("user", "account"),
            "msg": msgText.get(1.0, END),
            "log": text.get(1.0, END)
        }
        resp = requests.post(
            'http://rolin.icu:22222/api/feedback', data=data, timeout=15)
        print(resp.text)

        if resp.text == "ok":
            tkinter.messagebox.showinfo("Success", "发送成功！我们将会尽快解决问题")
            fbw.destroy()
        else:
            tkinter.messagebox.showinfo("失败", "发送失败")
            fbw.destroy()

    sumbit.bind('<Button-1>', sendMsg)


if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    configWindow(root, 1)
    root.mainloop()
