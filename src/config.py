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
def buildParam(account,password,ip):
    body = {
        'c': 'Portal',
        'a': 'login',
        'login_method': '1',
        'user_account': ',0,{}'.format(account),
        'user_password': password,
        'wlan_user_ip':  ip
    }
    return body


# URL
UPDATE_URL = "http://net.30202.co/update?xuehao={}&ip={}"
SELECT_URL = "http://net.30202.co/"
OFFICIAL_WEB = "https://www.gdqy.edu.cn/"
INDEX_BILIBILI = "https://space.bilibili.com/23161464"
# 常用常量
GET_IP_WAIT_TIME = 10

# 系统常量
VERSION = '4.0.0'
