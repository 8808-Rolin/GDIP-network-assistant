'''
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-09-18 22:04:58
LastEditors: Rolin
Code-Function-What do you want to do: 其他窗口
'''
from tkinter import *
import tkinter.messagebox  # 这个是消息框，对话框的关键
import utils


def configWindow(root, text, type=0):
    # 获取配置文件
    config = utils.getConfig()

    cw = Toplevel(root)
    cw.grab_set()
    cw.geometry('300x370')
    cw.iconbitmap('favicon.ico')
    cw.title('Setting')
    cw.resizable(0, 0)  # 防止用户调整尺寸
    accLable = Label(master=cw, width=7, height=1, text="账号：")
    pwdLable = Label(master=cw, width=7, height=1, text="密码：")
    timeLable = Label(master=cw, width=8, height=1, text="等待时间：")
    ipLable = Label(master=cw, width=21, height=1, text="当前IP：{}".format(utils.get_ip(text)))

    accText = Entry(master=cw, width=20)
    pwdText = Entry(master=cw, width=20)
    timeText = Entry(master=cw, width=20)


    saveBtn = Button(master=cw, height=2, width=15, text='保存')
    quitBtn = Button(master=cw, height=2, width=15,
                        text='退出', command=cw.destroy)

    accLable.place(x=30, y=30)
    pwdLable.place(x=30, y=90)
    timeLable.place(x=30, y=160)
    ipLable.place(x=30, y=230)
    accText.place(x=100, y=30)
    pwdText.place(x=100, y=90)
    timeText.place(x=100, y=160)
    saveBtn.place(x=35, y=310)
    quitBtn.place(x=160, y=310)

    accText.insert(0, config.get("user", "account"))
    pwdText.insert(0, config.get('user', 'password'))
    timeText.insert(0, config.get("system", "sleepTime"))

    # 保存新的配置文件
    def save(elf):
        # 获取config对象
        config = utils.getConfig()

        acc = accText.get()
        pwd = pwdText.get()
        time = timeText.get()

        config.set("system", "sleepTime", time)
        config.set("user", "account", acc)
        config.set("user", "password", pwd)
        try:
            config.write(open("config\\config.ini", "r+"))
            utils.addText(text, "---更新设置成功  当前设置如下---")
            utils.addText(text, "校园网账号：{}".format(acc))
            utils.addText(text, "等待重连的时间：{}秒".format(time))
            cw.destroy()
            tkinter.messagebox.showinfo("Success", "保存设置成功！")
        except Exception as e:
            utils.addText(text,str(e))
            tkinter.messagebox.showinfo("Failure", "保存设置失败，请重试")
    saveBtn.bind("<Button-1>", save)



if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    configWindow(root, 1)
    root.mainloop()
