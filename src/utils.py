'''
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-11-05 01:01:57
LastEditors: Rolin
Code-Function-What do you want to do: 工具方法
'''
import configparser
import json
import time
import uuid
import webbrowser
from subprocess import PIPE, run
from tkinter import *
from tkinter import filedialog

import requests

import config
import re
import network
from log import *

cf = configparser.ConfigParser()


# 通过校园网获取IP
def get_ip(text):
    logger = log(text)
    try:
        resp = requests.get(config.IP_URL, timeout=10)
        resp.keep_alive = False
        logger.info("获取IP中>>>  请求响应码：{}".format(resp.status_code))
    except Exception as e:
        logger.war("获取IP失败，请检查你的网络,具体错误请查看日志")
        logger.error(str(e))
        return ""

    try:
        # 处理响应结果
        res = url2json(config.IP_URL, text=text)

        if "v46ip" in res:
            logger.info("获取IP成功，你当前的IP为：{}".format(res['v46ip']))
            return res['v46ip']
        else:
            logger.war("获取IP失败，请检查你的网络")
            return ""
    except Exception as e:
        logger.war("后台错误，获取IP失败，请检查你的网络")
        logger.error(str(e))
        return ""


# 重复获取IP直至获取成功
def get_true_ip(text):
    logger = log(text)
    # 获取IP
    while True:
        ip = get_ip(text)
        if ip != "":
            return ip
        logger.info("正在重试获取ip地址")
        time.sleep(config.GET_IP_WAIT_TIME)


# 连通性测试
def pingBaidu(text):
    logger = log(text)
    r = run('ping 114.114.114.114',
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
            shell=True)
    if r.returncode:
        logger.war("连通测试(ping)失败！判断当前网络已断开！")
    else:
        logger.info("连通测试(ping)成功！当前网络正常！")


# 进行一个日志的导
def exportLog(text):
    logger = log(text)
    log_text = text.get('1.0', END)
    folder_path = filedialog.askdirectory(initialdir="./")
    if folder_path:
        localtime = time.strftime("%Y-%m-%d", time.localtime())
        file_path = "{0}/NetworkLog_{1}-{2}.log".format(
            folder_path, localtime, uuid.uuid1())
        loge = open(file_path, "w")
        loge.write(log_text)
        logger.info("导出日志文件成功，文件路径：{0}".format(file_path))
        loge.close()


def updateIP(account, text):
    logger = log(text)
    try:
        ip = get_true_ip(text)
        # 在此处撰写同步更新IP代码
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        uri = config.UPDATE_URL.format(
            account, ip, config.VERSION)
        res = requests.get(url=uri)
        # 输出日志
        logger.debug(res.text)
        result = json.loads(res.text)

        if result['status'] == 1:
            logger.info("同步IP成功")
            return True
        else:
            logger.war("同步IP失败，请联系开发者")
            return False
    except Exception as err:
        logger.error(str(err))
        logger.war("同步IP出错了，等下再试把")
        return False


def statusBarCallback(self):
    webbrowser.open_new(config.INDEX_BILIBILI)


def getConfig():
    cf.read('config\\config.ini', encoding='UTF-8')
    return cf


def get_account(text):
    logger = log(text)
    logger.info("---自动获取学号----")
    try:
        resp = requests.get(config.IP_URL, timeout=10)
        logger.info("尝试获取账号中>>>  请求响应码：{}".format(resp.status_code))
    except Exception as e:
        logger.error(str(e))
        logger.war("获取学号失败，请在设置中填写学号。")
        return ""

    try:
        # 处理响应结果
        res = url2json(config.IP_URL, text=text);
        if "uid" in res:
            logger.info("获取学号成功，你当前的学号为：{}".format(res['uid']))
            return res['uid']
        else:
            return ""
    except Exception as e:
        logger.error(str(e))
        logger.war("获取学号失败，请在设置中填写学号。")
        return ""


# Update Status Bar Content Thread
# 实时更新状态栏内容线程
def usbct(statusbar, text):
    logger = log(text)
    # 初始化状态栏
    # 检测当前状态
    # 更新任务栏内容
    while True:
        sbstr = "校园网助手Ver{}守护你的网络中...... ".format(config.VERSION)
        try:
            # 获取登录状态
            status = isLoin(text)
            if not status:
                sbstr += '\t 当前还未成功登录校园网，正在登陆校园网......'
                statusbar['text'] = sbstr
                time.sleep(1.5)
                continue
            # 当登陆成功后显示个人信息
            rq2 = requests.get(timeout=5, url=config.INDEX_LOGIN)
            lip = re.findall(
                pattern=config.LAST_LOGIN_IP_PATTERN, string=rq2.text)
            stime = re.findall(
                pattern=config.LAST_START_TIME_PATTERN, string=rq2.text)
            etime = re.findall(
                pattern=config.LAST_END_TIME_PATTERN, string=rq2.text)
            NID = re.findall(
                pattern=config.LAST_NAME_ID_PATTERN, string=rq2.text)

            sbstr += '\t 上次登录IP：{}，上次登录时间：{}，上次登出时间：{}，用户名称：{}'.format(
                lip[0], stime[0], etime[0], NID[0])
            statusbar['bg'] = 'green'
            statusbar['text'] = sbstr
            time.sleep(15)
        except Exception as e:
            logger.war(str(e))
            statusbar['bg'] = 'red'
            for i in range(5, 0):
                sbstr = "校园网助手连接出错,将在{}秒后进行重试".format(i)
                statusbar['text'] = sbstr
                time.sleep(1)


# 通过校园网抓包可获取用户当前登陆状态
def isLoin(text):
    try:
        resp_json = url2json(config.IP_URL, text)
        return resp_json['result'] == 1
    except Exception as e:
        return False


# 将常见的url请求结果去掉括号后生成一个json
# 仅使用于响应格式为：dr100x({ ... })的请求
def url2json(url, text, timeout=5, param=None):
    if param is None:
        param = {}
    logger = log(text)
    rq1 = requests.get(url, params=param, timeout=timeout)
    logger.debug("请求结果>>>  请求响应码：{}".format(rq1.status_code))
    result = rq1.text.split('(')
    result = result[1].split(")")
    result = result[0]
    logger.debug(result)
    return json.loads(result)
