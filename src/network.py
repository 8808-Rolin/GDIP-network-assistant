'''
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-11-05 01:02:07
LastEditors: Rolin
Code-Function-What do you want to do: 网络相关方法
'''

import utils
import config as cf
import time
import requests
import json
import base64
import configparser
from subprocess import PIPE, run



# 登陆校园网
def login(account,password,text):
    #获取ip
    ip = utils.get_true_ip(text)

    param = cf.buildParam(account,password,ip)
    utils.addText(text, "当前校园网账号>>> {}".format(account))
    utils.addText(text, "当前校园网IP>>> {}".format(ip))
    # 发送请求
    rq = requests.get(cf.LOGIN_URL, params=param, timeout=10)
    utils.addText(text, "请求结果>>>  请求响应码：{}".format(rq.status_code))
    
    if rq.status_code != 200:
        utils.addText(text, "页面请求出现错误！")
        return False

    # 处理响应数据
    result = rq.text.split('(')
    result = result[1].split(")")
    result = result[0]
    res = json.loads(result)

    if("ret_code" in result):
        ret_code = json.loads(result)["ret_code"]
    else:
        ret_code = -1
    

    # 结果判定
    if res['result'] == "1":
        utils.addText(text, ">>>{}".format(res['msg']))
        return True
    elif res['result'] == "0" and ret_code == 2:
        utils.addText(text, ">>>您已经成功登录,无需再次登录")
        return True
    elif res['result'] == "0" and ret_code == 1:
        msg = base64.b64decode(res['msg'].encode()).decode
        utils.addText(text,">>>{}".format(msg))
        return False
    else:
        msg = res['msg']
        utils.addText(text, "错误信息>>>{}".format(result))
        utils.addText(text, ">>>{}".format(msg))
        return False


# 脚本运行
def scriptRun(text,sb):
    utils.addText(text, '----脚本开始运行----')
    utils.addText(
        text, 'Welcom To Use GDIP Network Assistant Version {}  For Windows'.format(cf.VERSION))

    # 引入配置文件
    # 实例化configParser对象
    config = configparser.ConfigParser()
    # read读取ini文件
    config.read('config\\config.ini', encoding='UTF-8')
    

    # 用户参数
    account = config.get('user', 'account')
    password = config.get('user', 'password')
    sleepTime = eval(config.get('system', 'sleepTime'))  # 睡眠时间

    # 提示信息
    utils.addText(text, "校园网账号：{}".format(account))
    utils.addText(text, "重连时间：{}秒".format(sleepTime))

    # 连接校园网
    cnt = 1 #重连次数
    testnum = 0 
        # 判断当前是否网络正常
    while True:
        r = run('ping 114.114.114.114',
                stdout=PIPE,
                stderr=PIPE,
                stdin=PIPE,
                shell=True)
                
        # 没有网络时
        if r.returncode:
            sb['bg'] = "red"

            utils.addText(
                text, '校园网已断开，正在重连 第{0}次'.format(cnt))

            config.read('config\\config.ini', encoding='UTF-8')
            account = config.get('user', 'account')
            password = config.get('user', 'password')
            sleepTime = eval(config.get('system', 'sleepTime'))  # 睡眠时间

            try:
                if login(account, password, text) :
                    testnum = 0
                    cnt += 1
                    continue
                else:
                    utils.addText(text, "重连错误！！！，将在{}秒后重连".format(sleepTime))
                    testnum = 0
                    cnt += 1
                    time.sleep(sleepTime)
                    continue
            except Exception as e:
                utils.addText(text, "重连错误！！！，将在{}秒后重连".format(sleepTime))
                time.sleep(sleepTime)
                testnum = 0
                cnt += 1
                continue
        else:
            sb['bg'] = "green"
            if (testnum % 120) == 0:
                utils.addText(text, '当前网络状态正常')
                # 更新网站上的ip
                utils.updateIP(account,text)
            testnum += 1
        # 定时心跳
        time.sleep(sleepTime)


def linkNet(text):
    config = configparser.ConfigParser()
    config.read('config\\config.ini', encoding='UTF-8')
    account = config.get('user', 'account')
    password = config.get('user', 'password')

    login(account, password, text)
