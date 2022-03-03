#   运行在Linux上的校园网自动登陆脚本
#   简单，可靠的运行,完整详细的日志跟踪
#   24x7全天候运行

from time import strftime
import requests
import configparser
import os
import time
import json
import base64

# 正则表达式
LAST_LOGIN_IP_PATTERN = r'lip=\'(.*?)\';'
LAST_START_TIME_PATTERN = r'stime=\'(.*?)\';'
LAST_END_TIME_PATTERN = r'etime=\'(.*?)\';'
LAST_NAME_ID_PATTERN = r'NID=\'(.*?)\';'

# 1. 获取配置文件，若没有配置文件则退出程序

cf = configparser.ConfigParser()
cf.read(os.path.abspath('config.ini'))  # 读取配置文件
secs = cf.sections()
if secs == []:
    exit(-1)

account = cf.get('userdata','acc')
password = cf.get('userdata','pwd')

stime = cf.get('sysdata','sleep')

print('软件初始化完毕，校园网用户：{},欢迎你。'.format(account))

# 2. 方法体
IP_URL = cf.get('urldata',"IP_URL")

# 通过校园网抓包可获取用户当前登陆状态
def isLoin():
    try:
        resp_json = url2json(IP_URL)
        return resp_json['result'] == 1
    except Exception as e:
        return False


# 将常见的url请求结果去掉括号后生成一个json
# 仅使用于响应格式为：dr100x({ ... })的请求
def url2json(url,timeout=5, param=None):
    if param is None:
        param = {}
    rq1 = requests.get(url, params=param, timeout=timeout)
    print("请求结果>>>  请求响应码：{}".format(rq1.status_code))
    result = rq1.text.split('(')
    result = result[1].split(")")
    result = result[0]
    print(result)
    return json.loads(result)

# 通过校园网获取IP

def get_ip():
    try:
        resp = requests.get(IP_URL, timeout=10)
        resp.keep_alive = False
        print("获取IP中>>>  请求响应码：{}".format(resp.status_code))
    except Exception as e:
        print("获取IP失败，请检查你的网络,具体错误请查看日志")
        print(str(e))
        return ""

    try:
        # 处理响应结果
        res = url2json(IP_URL)

        if "v46ip" in res:
            print("获取IP成功，你当前的IP为：{}".format(res['v46ip']))
            return res['v46ip']
        else:
            print("获取IP失败，请检查你的网络")
            return ""
    except Exception as e:
        print("后台错误，获取IP失败，请检查你的网络")
        print(str(e))
        return ""

def get_true_ip():
    # 获取IP
    while True:
        ip = get_ip()
        if ip != "":
            return ip
        print("正在重试获取ip地址")
        time.sleep(1)

# 登陆校园网
def login(account, password):
    # 获取ip
    ip = get_true_ip()
    
    param = {
        'c': 'Portal',
        'a': 'login',
        'login_method': '1',
        'user_account': ',0,{}'.format(account),
        'user_password': password,
        'wlan_user_ip': ip
    }
    print("当前校园网账号>>> {}".format(account))
    print("当前校园网IP>>> {}".format(ip))
    print("当前校园网IP>>> {}".format(ip))
    # 发送请求
    try:

        res = url2json(cf.get('urldata','LOGIN_URL'),timeout=10,param=param)
        # 日志打印JSON结果
        print(res)

        if "ret_code" in res:
            ret_code = res["ret_code"]
        else:
            ret_code = -1

        # 结果判定
        if res['result'] == "1":
            print(">>>{}".format(res['msg']))
            return True
        elif res['result'] == "0" and ret_code == 2:
            print(">>>您已经成功登录,无需再次登录")
            return True
        elif res['result'] == "0" and ret_code == 1:
            msg = base64.b64decode(res['msg'].encode()).decode
            print(">>>{}".format(msg))
            return False
        else:
            msg = res['msg']
            print("错误信息>>>{}".format(res))
            print(">>>{}".format(msg))
            return False
    except Exception as e:
        print("登录错误！，详细信息请查看日志文件")
        print(str(e))
        return False

# 3. 循环业务
# 判断当前是否网络正常，才是校验登录的方式
while True:
    sleep_time = eval(stime)  # 睡眠时间
    is_login = isLoin()
    # 没有网络时
    if not is_login:
        print('校园网已断开，正在重连...')
        try:
            if login(account, password):
                continue
            else:
                print("重连错误！！！，将在{}秒后重连".format(sleep_time))
                time.sleep(sleep_time)
                continue
        except Exception as e:
            print("重连错误！！！，将在{}秒后重连,详细错误请查看日志".format(sleep_time))
            print(str(e))
            time.sleep(sleep_time)
            continue
    else:
        print('当前网络状态正常')
    # 定时心跳
    time.sleep(sleep_time)