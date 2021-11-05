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
from pathlib import Path

image_image_1 = None
entry_image_1 = None
entry_image_2 = None
entry_image_3 = None
button_image_1 = None
button_image_2 = None
OUTPUT_PATH = None
ASSETS_PATH = None


def configWindow(root,text,type = 0):
    global image_image_1
    global entry_image_1
    global entry_image_2
    global entry_image_3
    global button_image_1
    global button_image_2
    global OUTPUT_PATH
    global ASSETS_PATH
    #读取资源文件
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    # 获取配置文件
    config = utils.getConfig()
    cw = Toplevel(root)
    cw.geometry("280x403")
    cw.configure(bg = "#FFFFFF")
    cw.iconbitmap('./assets/favicon.ico')
    cw.title('Setting')
    cw.resizable(0, 0)

    # 控件绘制
    # 背景绘制
    canvas = Canvas(bg = "#FFFFFF",height = 403,width = 280,bd = 0,highlightthickness = 0,relief = "ridge",master=cw)
    canvas.place(x = 0, y = 0)
    #顶图绘制
    image_image_1 = PhotoImage(file=relative_to_assets("image_01.png"))
    image_1 = canvas.create_image(140.0,48.0,image=image_image_1)
    # 学号输入框绘制
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_01.png"))
    entry_bg_1 = canvas.create_image(140.5,150.0,image=entry_image_1)
    accText = Entry(bd=0,bg="#eff6fb",highlightthickness=0,master=cw)
    accText.place(x=38.0,y=138.0,width=203.0,height=22.0)
    # 密码输入框绘制
    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(141.5,216.0,image=entry_image_2)
    pwdText = Entry(bd=0,bg="#eff6fb",highlightthickness=0,master=cw)
    pwdText.place(x=38.0,y=204.0,width=203.0,height=22.0)
    # 等待时间输入框绘制
    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(174.0,263.5,image=entry_image_3)
    timeText = Entry(bd=0,bg="#eff6fb",highlightthickness=0,master=cw)
    timeText.place(x=100.0,y=252.0,width=150.0,height=21.0)
    # 文字绘制
    canvas.create_text(32.0,112.0,anchor="nw",text="学号：",fill="#000000",font=("Roboto", 18 * -1))
    canvas.create_text(32.0,178.0,anchor="nw",text="密码：",fill="#000000",font=("Roboto", 18 * -1))
    canvas.create_text(20.0,256.0,anchor="nw",text="重连时间(s)",fill="#000000",font=("Roboto", 14 * -1))
    canvas.create_text(53.0,294.0,anchor="nw",text="当前IP：{}".format(utils.get_ip(text)),fill="#000000",font=("Roboto", 16 * -1))
    # 保存按钮绘制
    button_image_1 = PhotoImage(file=relative_to_assets("button_01.png"))
    saveBtn = Button(image=button_image_1,borderwidth=0,highlightthickness=0,relief="flat",
        command=lambda: print("button_1 clicked"),master=cw)
    saveBtn.place(x=34.0,y=346.0,width=96.0,height=32.0)
    # 退出按钮绘制
    button_image_2 = PhotoImage(file=relative_to_assets("button_02.png"))
    quitBtn = Button(image=button_image_2,borderwidth=0,highlightthickness=0,relief="flat",
        command=cw.destroy,master=cw)
    quitBtn.place(x=150.0,y=346.0,width=96.0, height=32.0)

    # 插入数值
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
