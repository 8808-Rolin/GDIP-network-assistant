'''
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-11-05 09:59:59
LastEditors: Rolin
Code-Function-What do you want to do: 存放常量配置
'''
# 获取IP部分参数
IP_URL = "http://10.0.0.37/drcom/chkstatus?callback=dr1002"

# 登录校园网部分参数
LOGIN_URL = "http://10.0.0.37:801/eportal/"


def buildParam(account, password, ip):
    body = {
        'c': 'Portal',
        'a': 'login',
        'login_method': '1',
        'user_account': ',0,{}'.format(account),
        'user_password': password,
        'wlan_user_ip': ip
    }
    return body


# URL
UPDATE_URL = "http://net.30202.co/update?xuehao={}&ip={}&version={}"
SELECT_URL = "http://net.30202.co/"
OFFICIAL_WEB = "https://www.gdqy.edu.cn/"
INDEX_BILIBILI = "https://space.bilibili.com/23161464"
INDEX_LOGIN = "http://10.0.0.37/"
# 常用常量
GET_IP_WAIT_TIME = 10

# 系统常量
VERSION = '4.2.0'

# 正则表达式
LAST_LOGIN_IP_PATTERN = r'lip=\'(.*?)\';'
LAST_START_TIME_PATTERN = r'stime=\'(.*?)\';'
LAST_END_TIME_PATTERN = r'etime=\'(.*?)\';'
LAST_NAME_ID_PATTERN = r'NID=\'(.*?)\';'

# Tips Text
OPEN_WARNING = "你当前没有连接到任何网络，软件可能不会正常工作。\n如果你当前使用网线连接校园网，那么可能校园网机房出问题了\n待网络恢复后软件会自行连接"
OPEN_STOP = "你当前没有连接到广东轻工职业技术学院的校园网环境\n继续运行程序可能会产生大量的错误日志文件\n建议切换到校园网环境下再启动该软件\n---是否现在进入软件---"
