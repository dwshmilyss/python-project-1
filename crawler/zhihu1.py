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

def test1():
    requests_session, requests_cookies = create_session()
    url = 'http://www.zhihu.com'
    reqs = requests_session.get(url, cookies=requests_cookies)  # 已登陆
    # content = reqs.content
    res = requests.get(url)
    res = res.text.encode(res.encoding).decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    print soup
    exit()
    # 获取登录用户名
    user_name = soup.find("div", class_="top-nav-profile").a.span.string
    print "user_name:%s" % (user_name)
    # 获取用户头像地址
    pic_url = soup.find("div", class_="top-nav-profile").a.img
    # 下载用户头像
    urllib.urlretrieve(pic_url['src'], '/home/zeus/pic1/' + '1.jpg')
    print "potos:%s" % (pic_url['src'])
    # 获取前10个话题的内容
    for topic in soup.find_all("div", class_="feed-main", limit=10):
        print '-------------------------------------------------------'
        # 获取知乎问题来源
        topic_source = topic.find("div", class_="feed-source").a.get_text()
        print "topic source:%s" % (topic_source)
        # 获取知乎问题
        question = topic.find("div", class_="content").a.get_text()
        print "question:%s" % (question)
        # 获取该问题被赞次数
        votecount = topic.find("div", class_="zm-item-vote").a.get_text()
        print "votecount:%s" % (votecount)
        # 获取问题回答者的用户名
        answer = topic.find("div", class_="zm-item-rich-text js-collapse-body")
        if answer:
            print "answer_name:%s" % (answer['data-author-name'])
        print '-------------------------------------------------------'


def test2():
    url = "https://www.zhihu.com/api/v4/questions/36132174/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=10&offset=0&status=open"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        'Connection': 'keep-alive',
        'Cookie': 'd_c0="AFACknHv6guPTt9n7tt_ujGF_FGMCKRmOa0=|1497524803"; _zap=a52d1e3b-ef2b-4b5f-9854-c6ed1db69d4b; capsion_ticket="2|1:0|10:1499942161|14:capsion_ticket|44:YzViNWI0OTgxMWJmNDBkOWE3NDBlZmVhZTc1MDQxY2E=|6f36e4f9393170344d464bbfe758bafa037aeeddd2ac6f8ae7c1ec72e2b46165"; aliyungf_tc=AQAAAOWcEUdnBAAAqzX3OtNi2yHDvcGF; q_c1=e3013990341248c4a3e38c4bda43a059|1500264832000|1494214710000; infinity_uid="2|1:0|10:1500272224|12:infinity_uid|24:ODcwMjg1NDY1OTM1MzAyNjU2|a31c28d6326d96f880c3ffebb1dc0904d41467f4d373629d0da2159be1653ef0"; __utmt=1; __utma=51854390.400069527.1500272434.1500272434.1500272434.1; __utmb=51854390.0.10.1500272434; __utmc=51854390; __utmz=51854390.1500272434.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20161130=1^3=entry_date=20161130=1; l_cap_id="YTQ5NjJiZjg5ZDg0NGUyOGExNzUyN2FkNjljZGRjMzE=|1500272575|3009bab9808a3fa5dda3bcfcda27e9c7558a9e8c"; r_cap_id="Njk2MjY0ODAyZmM3NGY2N2EzZmFlZjZiM2M0YTJhZWU=|1500272575|8cb4f52ac8866977a212ba2982a92fb600b32a78"; cap_id="MWVlZDM0Y2U5NWI0NDM0NDg5MTdhZDBjMzI0Mzk4YjA=|1500272575|8da455e6859854587ba885db74b6a8c991fe0e3c"; _xsrf=099e2296-f1ee-4dc5-b872-461c5f2483ce',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/question/36132174',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'x-udid': 'AFACknHv6guPTt9n7tt_ujGF_FGMCKRmOa0='
    }
    res = requests.get(url,headers = headers)
    print res.content
    print res.text
    exit()

if __name__ == '__main__':
    test2()
    pass





