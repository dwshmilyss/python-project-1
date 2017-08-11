#!/usr/bin/env python
# encoding: utf-8
#导入需要的python模块httplib，用来模拟提交http请求，详细的用法可见python帮助手册

import httplib

#导入需要的python模块urllib，用来对数据进行编码
import urllib

import sys
default_encoding="utf-8"
if(default_encoding!=sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)
"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: http.py
@time: 2017/7/12 14:01
"""


def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == "__main__":
    reqheaders = {'Connection': 'keep-alive',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Host': 'weixin.sogou.com',
                  'Referer': 'http://weixin.sogou.com/weixin?type=2&s_from=input&query=%E5%B7%B4%E5%9F%BA%E6%96%AF%E5%9D%A6%E6%81%90%E8%A2%AD&ie=utf8&_sug_=n&_sug_type_=',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
                  'Upgrade-Insecure-Requests':'1',
                  'Accept - Encoding': 'gzip, deflate',
                  'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                  }

    # conn = httplib.HTTPConnection('10.21.3.93:38080')
    conn = httplib.HTTPConnection('weixin.sogou.com')
    # url = 'http://10.21.3.93:38080/rsa_service/servlet/RSAServlet?userName=10000347&passCode=120653459887'
    url = 'http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E5%B7%B4%E5%9F%BA%E6%96%AF%E5%9D%A6%E6%81%90%E8%A2%AD&tsn=5&ft=2017-07-12&et=2017-07-12&interation=&wxid=&usip='
    conn.request(method="GET", url=url,headers=reqheaders)
    response = conn.getresponse()
    res = response.read()
    print res
    pass