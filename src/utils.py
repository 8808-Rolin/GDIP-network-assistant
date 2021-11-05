'''
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-11-05 01:01:57
LastEditors: Rolin
Code-Function-What do you want to do: 工具方法
'''
import webbrowser
import config
import requests
from tkinter import *
import json
from subprocess import PIPE, run
from tkinter import filedialog
import time
import uuid
import configparser

# 打印数据
def addText(text, str):
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    str = localtime+"->"+str + "\n"
    text.configure(state='normal')
    text.insert(END, str)
    text.configure(state='disabled')


# 通过校园网获取IP
def get_ip(text):
    try:
        resp = requests.get(config.IP_URL, timeout=10)
        addText(text, "获取IP中>>>  请求响应码：{}".format(resp.status_code))
    except:
        addText(text, "网络错误，获取IP失败，请检查你的网络")
        return ""

    if resp.status_code != 200 :
        addText(text, "请求错误，获取IP失败，请检查你的网络")
        return ""
    try:
        #处理响应结果
        result = resp.text.split('(')
        result = result[1].split(")")
        result = result[0]
        res = json.loads(result)
        
        if "v46ip" in result:
            addText(text, "获取IP成功，你当前的IP为：{}".format(res['v46ip']))
            return res['v46ip']
        else:
            addText(text, "响应错误，获取IP失败，请检查你的网络")
            return ""
    except:
        addText(text, "后台错误，获取IP失败，请检查你的网络")
        return ""
    

## 重复获取IP直至获取成功
def get_true_ip(text):
    #获取IP
    while True:
        ip = get_ip(text)
        if ip != "":
            return ip
        addText(text, "正在重试获取ip地址")
        time.sleep(config.GET_IP_WAIT_TIME)

# 连通性测试
def pingBaidu(text):
    r = run('ping www.baidu.com',
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
            shell=True)
    if r.returncode:
        addText(text, "连通测试(ping)失败！判断当前网络已断开！")
    else:
        addText(text, "连通测试(ping)成功！当前网络正常！")

# 进行一个日志的导
def exportLog(text):
    logText = text.get('1.0', END)
    folderPath = filedialog.askdirectory(initialdir="./")
    if folderPath:
        localtime = time.strftime("%Y-%m-%d", time.localtime())
        filePath = "{0}/NetworkLog_{1}-{2}.log".format(
            folderPath, localtime, uuid.uuid1())
        log = open(filePath, "w")
        log.write(logText)
        addText(text, "导出日志文件成功，文件路径：{0}".format(filePath))
        log.close()

def updateIP(account,text):
    try:
        ip = get_true_ip(text)
        # 在此处撰写同步更新IP代码
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        uri = config.UPDATE_URL.format(
            account, ip)
        res = requests.get(url=uri)
        result = json.loads(res.text)
        if(result['status'] == 1):
            addText(text, "同步IP成功")
            return True
        else:
            addText(text, "同步IP失败，请联系开发者")
            return False
    except Exception as err:
        addText(text, str(err))
        addText(text, "同步IP出错了，等下再试把")
        return False

def statusBarCallback():
    webbrowser.open_new(config.INDEX_BILIBILI)


def getConfig():
    cf = configparser.ConfigParser()
    cf.read('config\\config.ini', encoding='UTF-8')
    return cf
