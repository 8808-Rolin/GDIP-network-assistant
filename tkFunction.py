'''
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-09-18 21:01:14
LastEditors: Rolin
Code-Function-What do you want to do:
FilePath: \vscode-workspace\python\src\LoginNetwork\release\tkFunction.py
'''
import base64
import configparser
import json
import os
import socket
import time
from subprocess import PIPE, run
from time import sleep
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from types import TracebackType
import requests
import uuid
import webbrowser
import win32api
import win32con
import winreg
import webbrowser

global recursive
recursive = 1
account = ""
password = ""
ip = ""
sleepTime = ""
url = ""
# 获取实时IP


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return str(ip)

# 打印数据


def addText(text, str):
    str = str + "\n"
    text.configure(state='normal')
    text.insert(END, str)
    text.configure(state='disabled')

# 登陆校园网方法


def login(account, password, ip, url, text):
    global recursive
    # 构建数据
    # 生产环境
    dataOnServer = {
        'c': 'Portal',
        'a': 'login',
        'login_method': '1',
        'user_account': ',0,{}'.format(account),
        'user_password': password,
        'wlan_user_ip':  ip
    }
    # 构造URI并请求
    rq = requests.get(url, dataOnServer, timeout=10)

    addText(text, "请求结果>>>".format(url))
    addText(text, "请求响应码：{}".format(rq.status_code))

    # 处理JSON
    result = rq.text.strip("(")
    result = result.strip(")")

    addText(text, "校园网响应结果：{}".format(result))
    # 提取Json的Key
    msg = json.loads(result)["msg"]

    if("ret_code" in result):
        res = json.loads(result)["ret_code"]
    else:
        res = -1

    # 结果判断
    if(json.loads(result)["result"] == "1"):
        addText(text, msg)
        addText(text, "校园网登陆成功")
    else:
        addText(text, "登录未成功")
        if(msg == "" and res == 1):
            addText(text, "原因：参数错误,可能是IP或者账号密码出错")
        elif(msg == "" and res == 2):
            addText(text, "原因：已登录")
        else:
            restr = json.loads(result)["msg"]
            resmsg = base64.b64decode(restr.encode('utf-8')).decode("utf-8")
            addText(text, "错误原因：{0},正在尝试重试第{1}次".format(resmsg, recursive))
            recursive += 1
            if(recursive <= 8):
                login(account, password, ip, url, text)
                sleep(0.5)
            else:
                addText(text, "登陆校园网失败，请稍后重试")
                recursive = 1


# 脚本运行
def scriptRun(text, version, sb):
    addText(text, '----脚本开始运行----')
    addText(text, 'Welcom To Use GDIP Network Assistant Version {}  For Windows'.format(version))

    # 引入配置文件
    # 实例化configParser对象
    config = configparser.ConfigParser()
    # read读取ini文件
    config.read('config\\config.ini', encoding='UTF-8')

    # 用户参数
    account = config.get('user', 'account')
    password = config.get('user', 'password')
    sleepTime = eval(config.get('system', 'sleepTime'))  # 睡眠时间
    url = config.get('system', 'url')
    ip = config.get('system', 'ip')
    addText(text, "校园网账号：{}".format(account))
    addText(text, "当前电脑IP：{}".format(ip))
    addText(text, "重连时间：{}秒".format(sleepTime))

    cnt = 1
    testnum = 0
    while True:
        r = run('ping www.baidu.com',
                stdout=PIPE,
                stderr=PIPE,
                stdin=PIPE,
                shell=True)
        if r.returncode:
            sb['bg'] = "red"
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            addText(text, '校园网已断开，正在重连 第{0}次 当前时间：{1}'.format(cnt, localtime))

            config.read('config\\config.ini', encoding='UTF-8')
            account = config.get('user', 'account')
            password = config.get('user', 'password')
            sleepTime = eval(config.get('system', 'sleepTime'))  # 睡眠时间
            url = config.get('system', 'url')
            ip = config.get('system', 'ip')
            addText(text, "校园网账号：{}".format(account))
            addText(text, "当前校园网IP：{}".format(ip))

            try:
                login(account, password, ip, url, text)
            except Exception as e:
                addText(text, "重连错误！！！，将在{}秒后重连".format(sleepTime))
                sleep(sleepTime)
                continue
            testnum = 0
            cnt += 1
        else:
            sb['bg'] = "green"
            if (testnum % 120) == 0:
                addText(text, '当前网络状态正常')
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
            testnum += 1

        sleep(sleepTime)


def pingBaidu(text):
    # 引入配置文件
    # 实例化configParser对象
    config = configparser.ConfigParser()
    # read读取ini文件
    config.read('config\\config.ini', encoding='UTF-8')
    r = run('ping www.baidu.com',
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
            shell=True)
    if r.returncode:
        addText(text, "连通测试(ping)失败！判断当前网络已断开！")
    else:
        addText(text, "连通测试(ping)成功！当前网络正常！")


def linkNet(text):
    config = configparser.ConfigParser()
    config.read('config\\config.ini', encoding='UTF-8')
    account = config.get('user', 'account')
    password = config.get('user', 'password')
    url = config.get('system', 'url')
    ip = config.get('system', 'ip')
    addText(text, "校园网账号：{}".format(account))
    addText(text, "当前校园网IP：{}".format(ip))

    login(account, password, ip, url, text)


def exportLog(text):
    logText = text.get('1.0', END)
    folderPath = filedialog.askdirectory(initialdir="./")
    if folderPath:
        localtime = time.strftime("%Y-%m-%d", time.localtime())
        filePath = "{0}/NetworkScriptLog_{1}-{2}.log".format(
            folderPath, localtime, uuid.uuid1())
        log = open(filePath, "w")
        log.write(logText)
        addText(text, "导出日志文件成功，文件路径：{0}".format(filePath))
        log.close()


def openBilibili(self):
    webbrowser.open('https://space.bilibili.com/23161464',
                    new=0, autoraise=True)


def getConfig():
    config = configparser.ConfigParser()
    config.read('config\\config.ini', encoding='UTF-8')
    return config


def checkUpdate(version, root):
    n = requests.get("http://rolin.icu:22222/api/version", timeout=10)
    newversion = n.text

    if version == newversion:
        messagebox.showinfo("提示", "当前已是最新版本，无需更新")
    elif len(newversion) >= 15:
        messagebox.showinfo("ERROR", "出错了")
    else:
        if messagebox.askyesno("检查到新版本", "你的版本为：{0}\n当前最新版本为：{1}\n是否更新最新版本".format(version, newversion)):
            win32api.ShellExecute(0, 'open', 'update.exe', '', '', 1)
            root.quit()


'''
    Auto Checked Software Upadte When Application was started.
'''


def acu(version, text, root):
    sleep(1)
    nv = requests.get("http://rolin.icu:22222/api/version", timeout=10).text
    addText(text, "当前软件版本为:{}，最新版本为：{}\n".format(version, nv))
    # 如果版本不对则进行更新
    if not version == nv:
        if messagebox.askyesno("检查到新版本", "你的版本为：{0}\n当前最新版本为：{1}\n是否更新最新版本".format(version, nv)):
            win32api.ShellExecute(0, 'open', 'update.exe', '', '', 1)
            root.quit()


"""
    :param key_name: #  要查询的键名    
    :param reg_root: # 根节点
    # win32con.HKEY_CURRENT_USER
    # win32con.HKEY_CLASSES_ROOT
    # win32con.HKEY_CURRENT_USER
    # win32con.HKEY_LOCAL_MACHINE
    # win32con.HKEY_USERS
    # win32con.HKEY_CURRENT_CONFIG
    :param reg_path: #  键的路径
    :return:feedback是（0/1/2/3：存在/不存在/权限不足/报错）
"""


def Judge_Key(key_name,
              # 根节点  其中的值可以有：HKEY_CLASSES_ROOT、HKEY_CURRENT_USER、HKEY_LOCAL_MACHINE、HKEY_USERS、HKEY_CURRENT_CONFIG
              reg_root=win32con.HKEY_CURRENT_USER,
              reg_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",  # 键的路径
              ):
    reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
    try:
        key = winreg.OpenKey(reg_root, reg_path, 0, reg_flags)
        location, type = winreg.QueryValueEx(key, key_name)
        print("键存在", "location（数据）:", location, "type:", type)
        feedback = 0
    except FileNotFoundError as e:
        print("键不存在", e)
        feedback = 1
    except PermissionError as e:
        print("权限不足", e)
        feedback = 2
    except:
        print("Error")
        feedback = 3
    return feedback


"""
    :param switch: 注册表开启、关闭自启动
    :param zdynames: 当前文件名
    :param current_file: 获得文件名的前部分
    :param abspath: 当前文件路径
    :return:
"""


def AutoRun(switch="open",  # 开：open # 关：close
            zdynames='main.exe',
            current_file=None,
            abspath=os.path.abspath(os.path.dirname(__file__))):
    print(zdynames)

    path = abspath + '\\' + zdynames  # 要添加的exe完整路径如：
    judge_key = Judge_Key(reg_root=win32con.HKEY_CURRENT_USER,
                          reg_path=r"Software\Microsoft\Windows\CurrentVersion\Run",  # 键的路径
                          key_name=current_file)
    # 注册表项名
    KeyName = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key = win32api.RegOpenKey(
        win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
    if switch == "open":
        # 异常处理
        try:
            if judge_key == 0:
                print("已经开启了，无需再开启")
            elif judge_key == 1:
                win32api.RegSetValueEx(
                    key, current_file, 0, win32con.REG_SZ, path)
                win32api.RegCloseKey(key)
                print('开机自启动添加成功！')
        except:
            print('添加失败')
    elif switch == "close":
        try:
            if judge_key == 0:
                win32api.RegDeleteValue(key, current_file)  # 删除值
                win32api.RegCloseKey(key)
                print('成功删除键！')
            elif judge_key == 1:
                print("键不存在")
            elif judge_key == 2:
                print("权限不足")
            else:
                print("出现错误")
        except:
            print('删除失败')


def openPage():
    webbrowser.open("http://net.30202.co/")
