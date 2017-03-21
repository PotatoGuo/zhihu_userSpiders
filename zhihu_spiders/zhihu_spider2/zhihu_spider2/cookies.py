#encoding:utf-8
import requests
import re
import random

from user_agents import agents

"""知乎登录"""
accounts = [{'email':'yuhun17@sina.com', 'password':'19911117'}
            ]

def get_cookies():
    cookies = []
    for account in accounts:
        cookies.append(login(account['email'], account['password']))
        print '成功添加一个cookie'
    return cookies

def login(email, password):
    base_url = 'https://www.zhihu.com/#signin'
    session = requests.Session()
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI 5s Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.6.0'
    rep = session.request(method = 'get',url = base_url, headers = headers)
    _xsrf = re.search(re.compile(u'_xsrf.+?value="(.+?)"'), rep.text).group(1)
    url = 'https://www.zhihu.com/login/email'
    data = {'_xsrf':_xsrf,
    	'password':password,
    	'captcha_type':'cn',
    	'email':email
    	}
    response = session.request(method = 'post', url = url, data = data, headers = headers)
    cookie = session.cookies.get_dict()
    return cookie

cookies = get_cookies()
print '总共添加了%s个cookie' % str(len(cookies))
