#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: baidu.py
@time: 2017/7/7 16:18
"""
import os
import urllib
import httplib2
import webbrowser as web
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''
    利用urllib下载baidu的logo
'''
def test1():
    # 爬取在线网站
    url = "http://www.baidu.com/"
    '''
    首先我们调用的是urllib2库里面的urlopen方法，传入一个URL，这个网址是百度首页，协议是HTTP协议，当然你也可以把HTTP换做FTP、FILE、HTTPS 等等，只是代表了一种访问控制协议，urlopen一般接受三个参数，它的参数如下：
    urlopen(url, data, timeout)  
    第一个参数url即为URL，第二个参数data是访问URL时要传送的数据，第三个timeout是设置超时时间。
    第二三个参数是可以不传送的，data默认为空None，timeout默认为 socket._GLOBAL_DEFAULT_TIMEOUT。
    第一个参数URL是必须要传送的，在这个例子里面我们传送了百度的URL，执行urlopen方法之后，返回一个response对象，返回信息便保存在这里面。
    '''
    content = urllib.urlopen(url).read()
    open("baidu.html", "w").write(content)
    # 浏览求打开网站
    web.open_new_tab("baidu.html")

    # 下载图片 审查元素
    pic_url = "https://www.baidu.com/img/bd_logo1.png"
    pic_name = os.path.basename(pic_url)  # 删除路径获取图片名字
    print pic_name
    urllib.urlretrieve(pic_url, "d:/"+pic_name)

def test2():
    # Open PhantomJS
    # driver = webdriver.PhantomJS(executable_path="phantomjs-1.9.1-windows\phantomjs.exe")
    # driver = webdriver.Firefox()
    # 需要指定chromedriver的路径
    driver = webdriver.Chrome(executable_path="D:/10000347/Downloads/chromedriver_win32/chromedriver.exe")

    # 访问url
    driver.get("https://www.baidu.com/")

    print u'URL:'
    print driver.current_url
    # 当前链接: https://www.baidu.com/

    print u'标题:'
    print driver.title
    # 标题: 百度一下， 你就知道

    # print driver.page_source
    # 源代码

    # 定位元素，注意u1（数字1）和ul（字母L）区别
    print u'\n\n定位元素id:'
    info1 = driver.find_element_by_id("u1").text
    print info1

    # 定位元素
    print u'\n\n定位元素xpath:'
    info3 = driver.find_element_by_xpath("//div[@id='u1']/a")
    print info3.text

def callbackfunc(blocknum, blocksize, totalsize):
    '''''回调函数 
    @blocknum: 已经下载的数据块 
    @blocksize: 数据块的大小 
    @totalsize: 远程文件的大小 
    '''
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print "%.2f%%"% percent

class Main():
    def __init__(self):
        pass


if __name__ == "__main__":
    test2()
    pass