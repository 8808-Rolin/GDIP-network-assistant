"""
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-11-05 01:02:07
LastEditors: Rolin
Code-Function-What do you want to do: 网络相关方法
"""

import base64
from subprocess import PIPE, run

import config as cf
import utils
from log import *


# 登陆校园网
def login(account, password, text):
    logger = log(text)
    # 获取ip
    ip = utils.get_true_ip(text)

    param = cf.buildParam(account, password, ip)
    logger.info("当前校园网账号>>> {}".format(account))
    logger.info("当前校园网IP>>> {}".format(ip))
    logger.info("当前校园网IP>>> {}".format(ip))
    # 发送请求
    try:

        res = utils.url2json(cf.LOGIN_URL,timeout=10,param=param,text=text)
        # 日志打印JSON结果
        logger.debug(res)

        if "ret_code" in res:
            ret_code = res["ret_code"]
        else:
            ret_code = -1

        # 结果判定
        if res['result'] == "1":
            logger.info(">>>{}".format(res['msg']))
            return True
        elif res['result'] == "0" and ret_code == 2:
            logger.info(">>>您已经成功登录,无需再次登录")
            return True
        elif res['result'] == "0" and ret_code == 1:
            msg = base64.b64decode(res['msg'].encode()).decode
            logger.war(">>>{}".format(msg))
            return False
        else:
            msg = res['msg']
            logger.war("错误信息>>>{}".format(result))
            logger.war(">>>{}".format(msg))
            return False
    except Exception as e:
        log.war("登录错误！，详细信息请查看日志文件")
        log.error(str(e))
        return False


# 脚本运行
def scriptRun(text, sb):
    logger = log(text)
    logger.info('----脚本开始运行----')
    logger.addText(
        'Welcome To Use GDIP Network Assistant Version {}  For Windows'.format(cf.VERSION))

    config = utils.getConfig()
    # 用户参数
    account = config.get('user', 'account')
    sleep_time = eval(config.get('system', 'sleepTime'))  # 睡眠时间
    # 提示信息
    logger.addText("校园网账号：{}".format(account))
    logger.addText("重连时间：{}秒".format(sleep_time))

    # 连接校园网
    cnt = 1  # 重连次数
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

            logger.war(
                '校园网已断开，正在重连 第{0}次'.format(cnt))

            config.read('config\\config.ini', encoding='UTF-8')
            account = config.get('user', 'account')
            password = config.get('user', 'password')
            sleep_time = eval(config.get('system', 'sleepTime'))  # 睡眠时间

            try:
                if login(account, password, text):
                    testnum = 0
                    cnt += 1
                    continue
                else:
                    logger.war("重连错误！！！，将在{}秒后重连".format(sleep_time))
                    testnum = 0
                    cnt += 1
                    time.sleep(sleep_time)
                    continue
            except Exception as e:
                logger.war("重连错误！！！，将在{}秒后重连,详细错误请查看日志".format(sleep_time))
                logger.error(str(e))
                time.sleep(sleep_time)
                testnum = 0
                cnt += 1
                continue
        else:
            sb['bg'] = "green"
            if (testnum % 120) == 0:
                logger.info('当前网络状态正常')
                # 更新网站上的ip
                utils.updateIP(account, text)
            testnum += 1
        # 定时心跳
        time.sleep(sleep_time)


def linkNet(text):
    config = utils.getConfig()
    account = config.get('user', 'account')
    password = config.get('user', 'password')
    login(account, password, text)
