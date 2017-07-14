#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: __init__.py.py
@time: 2017/6/30 11:08
"""

import sys
default_encoding="utf-8"
if(default_encoding!=sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)
# 导入开发模块
import requests
from bs4 import BeautifulSoup
import os

import requests
import ConfigParser
from bs4 import BeautifulSoup
import re
import urllib
import urllib2

def create_session():
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    #从配置文件获取cookies值，并转化为dict
    cookies = cf.items('cookies')
    cookies = dict(cookies)
    from pprint import pprint
    pprint(cookies)
    #获取登录名
    phone_num = cf.get('info', 'phone_num')
    #获取登录密码
    password = cf.get('info', 'password')

    session = requests.session()
    login_data = {'phone_num': phone_num, 'password': password}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
        'Host': 'www.zhihu.com',
        'Referer': 'http://www.zhihu.com/'
    }
    #post登录
    r = session.post('http://www.zhihu.com/login/phone_num', data=login_data, headers=header)
    print r
    # if r.json()['r'] == 1:
    #     print 'Login Failed, reason is:',
    #     for m in r.json()['data']:
    #         print r.json()['data'][m]
    #     print 'So we use cookies to login in...'
    #     has_cookies = False
    #     for key in cookies:
    #         if key != '__name__' and cookies[key] != '':
    #             has_cookies = True
    #             break
    #     if has_cookies is False:
    #         raise ValueError('请填写config.ini文件中的cookies项.')
    #     else:
    #         r = session.get('http://www.zhihu.com/login/phone_num', cookies=cookies) # 用cookies登录

    return session, cookies


if __name__ == '__main__':
    requests_session, requests_cookies = create_session()
    url = 'http://www.zhihu.com'
    reqs = requests_session.get(url, cookies = requests_cookies) # 已登陆
    # content = reqs.content
    res = requests.get(url)
    res = res.text.encode(res.encoding).decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    print soup
    exit()
    #获取登录用户名
    user_name=soup.find("div",class_="top-nav-profile").a.span.string
    print "user_name:%s" % (user_name)
    #获取用户头像地址
    pic_url=soup.find("div",class_="top-nav-profile").a.img
    #下载用户头像
    urllib.urlretrieve(pic_url['src'],'/home/zeus/pic1/'+'1.jpg')
    print "potos:%s" %(pic_url['src'])
    #获取前10个话题的内容
    for topic in soup.find_all("div",class_="feed-main",limit=10):
        print '-------------------------------------------------------'
        #获取知乎问题来源
        topic_source=topic.find("div",class_="feed-source").a.get_text()
        print "topic source:%s" %(topic_source)
        #获取知乎问题
        question=topic.find("div",class_="content").a.get_text()
        print "question:%s" %(question)
        #获取该问题被赞次数
        votecount=topic.find("div",class_="zm-item-vote").a.get_text()
        print "votecount:%s" %(votecount)
            #获取问题回答者的用户名
        answer=topic.find("div",class_="zm-item-rich-text js-collapse-body")
        if answer:
            print "answer_name:%s" %(answer['data-author-name'])
        print '-------------------------------------------------------'





