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


