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

default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)
# 导入开发模块
import requests
from bs4 import BeautifulSoup
import os

import requests

try:
    import cookielib
except:
    import http_test.cookiejar as cookielib
import re
import time
import os.path

try:
    from PIL import Image
    from PIL import ImageEnhance
    from PIL import ImageFilter
except:
    pass

from pytesser import *

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'user-agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_xsrf():
    '''_xsrf 是一个动态变化的参数'''
    index_url = 'https://www.zhihu.com'
    # 获取登录时需要用到的_xsrf
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = r'name="_xsrf" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, html)
    return _xsrf[0]


# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


def login(secret, account):
    _xsrf = get_xsrf()
    headers["X-Xsrftoken"] = _xsrf
    headers["X-Requested-With"] = "XMLHttpRequest"
    # 通过输入的用户名判断是否是手机号
    if re.match(r"^1\d{10}$", account):
        print("手机号登录 \n")
        post_url = 'https://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': _xsrf,
            'password': secret,
            'phone_num': account
        }
    else:
        if "@" in account:
            print("邮箱登录 \n")
        else:
            print("你的账号输入有问题，请重新登录")
            return 0
        post_url = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': _xsrf,
            'password': secret,
            'email': account
        }
    # 不需要验证码直接登录成功
    login_page = session.post(post_url, data=postdata, headers=headers)
    login_code = login_page.json()
    if login_code['r'] == 1:
        # 不输入验证码登录失败
        # 使用需要输入验证码的方式登录
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.json()
        print(login_code['msg'])
    # 保存 cookies 到文件，
    # 下次可以使用 cookie 直接登录，不需要输入账号和密码
    session.cookies.save()


try:
    input = raw_input
except:
    pass

# 二值化
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

        # 由于都是数字
# 对于识别成字母的 采用该表进行修正
rep = {'O': '0',
       'I': '1', 'L': '1',
       'Z': '2',
       'S': '8'
       };


def getverify1(name):
    # 打开图片
    im = Image.open(name)
    # 转化到亮度
    imgry = im.convert('L')
    imgry.save('g' + name)
    # 二值化
    out = imgry.point(table, '1')
    out.save('b' + name)
    # 识别
    text = image_to_string(out)
    # 识别对吗
    text = text.strip()
    text = text.upper()

    # for r in rep:
    #     text = text.replace(r, rep[r])
    print text
    return text


if __name__ == '__main__':
    # im = Image.open('captcha.jpg')
    # print image_to_string(im)
    # if isLogin():
    if False:
        print('您已经登录')
        url = 'https://www.zhihu.com/settings/profile'
        res = session.get(url, headers=headers, allow_redirects=False)
        res = res.text.encode(res.encoding).decode('utf-8')
        soup = BeautifulSoup(res, 'html.parser')
        aa = soup.select_one('#rename-section > span').string
        print aa
    else:
        # account = input('请输入你的用户名\n>  ')
        # secret = input("请输入你的密码\n>  ")
        # account = '15902105647'
        # secret = 'dw8120653'
        # login(secret, account)
        url = 'https://www.zhihu.com/question/33892253'
        res = requests.get(url, headers=headers)
        print res.content
        # res = res.content.encode(res.encoding).decode('utf-8')


        from ghost import Ghost
        ghost = Ghost()
        with ghost.start() as session:
            page, extra_resources = session.open(url,headers=headers)
            print session.content
        # soup = BeautifulSoup(res, 'html.parser')
        # aa = soup.select('.QuestionHeader-title')
        # bb = soup.select('img .Avatar AuthorInfo-avatar')
        # cc = soup.select('a .UserLink-link')
        # # bb = soup.find(name='a', attrs={'class': 'UserLink-link'}).find(name='img',attrs = {'class' : 'Avatar AuthorInfo-avatar'})
        # print len(aa)
        # print soup
        # aa = soup.select_one('QuestionAnswers-answers > div:nth-child > div > div:nth-child > div:nth-child > div > div.RichContent.RichContent--unescapable > div.RichContent-inner > span > p')
        # bb = soup.select_one('#root > div > main > div > div:nth-child(10) > div.QuestionHeader > div.QuestionHeader-content > div.QuestionHeader-main > h1')
        # print bb
