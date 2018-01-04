#!/usr/bin/env python
# encoding: utf-8
#导入需要的python模块httplib，用来模拟提交http请求，详细的用法可见python帮助手册

import httplib
import base64
import zlib
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
import chardet
import json

def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == "__main__":
    reqheaders = {'Connection': 'keep-alive',
                  'Accept': '*/*',
                  'Host': 'kan.msxiaobing.com',
                  'Referer': 'https://kan.msxiaobing.com/ImageGame/Portal?task=yanzhi',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
                  'Upgrade-Insecure-Requests':'1',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
                  'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
                  'Origin':'https://kan.msxiaobing.com',
                  'Cookie':'ARRAffinity=3ef499a368f1faa276642c339ec894862f18dfbbad2c1c9406fdba05d3735640; cpid=4EhaM9hMxTBYSFM3eUksNcwwaLMbSSJNXkpCNF1L1DBKAA; salt=A70582D38F9AC74AD0CB72C88ECCDDE3'
                  }

    conn = httplib.HTTPConnection('kan.msxiaobing.com')

    image = open('4.jpg','rb')
    data = base64.b64encode(image.read())
    image.close()

    url = 'https://kan.msxiaobing.com/Api/Image/UploadBase64'
    conn.request(method="POST", url=url,headers=reqheaders,body=data)
    response = conn.getresponse()
    print response.getheaders()
    content = response.read()

    #因为API中response的header中有gzip  如果直接打印是乱码
    for key,value in response.getheaders():
        if str(key) == 'content-encoding' and str(value) == 'gzip':
            flag = True
            break
        else:
            flag = False
    if flag:
        html = zlib.decompress(content, 16 + zlib.MAX_WBITS)
    else:
        html = content
    result = chardet.detect(html)
    print html.decode("utf8")

    #解析返回的json字符串 拼装成图片上传后的URL 作为下次请求的参数
    jsonStr = html.decode("utf8")
    jsonObj = json.loads(jsonStr)
    jsonObj.get('Url')
    imageUrl = jsonObj.get('Host') + jsonObj.get('Url')
    print imageUrl

    if json:
        url = 'https://kan.msxiaobing.com/Api/ImageAnalyze/Process?service=yanzhi&tid=b6186eea75b5435fa938d2d91fe6cb03'
        params = {'MsgId':1515034104425,'CreateTime':1515034104,'Content[imageUrl]':imageUrl}
        params_urlencode = urllib.urlencode(params)
        conn.request(method="POST", url=url, headers=reqheaders, body=params_urlencode)

        response = conn.getresponse()
        print response.getheaders()
        content = response.read()

        # 因为API中response的header中有gzip  如果直接打印是乱码
        for key, value in response.getheaders():
            if str(key) == 'content-encoding' and str(value) == 'gzip':
                flag = True
                break
            else:
                flag = False
        if flag:
            html = zlib.decompress(content, 16 + zlib.MAX_WBITS)
        else:
            html = content
        result = chardet.detect(html)
        print html.decode("utf8")
    pass