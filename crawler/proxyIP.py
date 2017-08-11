#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: proxyIP.py
@time: 2017/8/11 10:32
"""
import sys

default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)

import urllib
import xlwt
import datetime
from bs4 import BeautifulSoup
import time

class GetProxyIp():
    def __init__(self,opener,):
        self.opener=opener

    def GetHtmlpage(self,url):
        html=self.opener.open(url)
        return html.read().decode("utf-8")

    def cleanHtml(self,html):
        #对网页进行清洗，获取IP,端口，类型，是否匿名，服务器地址
        ip=[]
        port=[]
        server_addr=[]
        Is_niming=[]
        type=[]
        time=[]
        soup=BeautifulSoup(html,"html.parser")
        #print(soup)
        try:
            ip_table=soup.find("table",id="ip_list")
            ip_result=ip_table.find_all("tr")

            for i in range(1,len(ip_result),1):
                result_td=ip_result[i].find_all("td")
                ip.append(result_td[1].string)
                port.append(result_td[2].string)
                try:
                    server_addr.append(result_td[3].a.string)
                except:
                    server_addr.append(result_td[3].string)
                Is_niming.append(result_td[4].string)
                type.append(result_td[5].string)
                time.append(result_td[9].string.split(" ")[0])
        except Exception:
            print(Exception)
            print("something wrong happened")
        return ip,port,server_addr,Is_niming,type,time

if __name__ == "__main__":

    #获取当前时间,并截除其前2位
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d")[2:]

    #创建一个opener
    import http
    cookie=http.cookiejar.CookieJar()
    cookieHandle=urllib.request.HTTPCookieProcessor(cookie)
    #proxy={"https":"https://222.85.50.64:808"}
    #proxyHandle=urllib.request.ProxyHandler(proxy)
    opener=urllib.request.build_opener(cookieHandle)
    #opener.add_handler(proxyHandle)

    #创建一个header，伪装成浏览器访问
    header=\
        {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
        }
    head=[]
    for key,value in header.items():
        enum=(key,value)
        head.append(enum)

    #为opener添加head
    opener.addheaders=head

    #需要爬取的地址
    url="http://www.xicidaili.com/nn/{num}/"

    Is_Over=True

    #实例化对象
    GPI=GetProxyIp(opener)
    #
    book=xlwt.Workbook()
    sheet=book.add_sheet(sheetname=currentTime)
    sheet.write(0, 0,"IP地址")
    sheet.write(0, 1, "端口")
    sheet.write(0, 2, "服务器地址")
    sheet.write(0, 3, "匿名")
    sheet.write(0, 4, "类型")
    sheet.write(0, 5 ,"日期")
    #初始化_num为1
    _num=1
    # 初始化位置为开头
    index = 0

    while(Is_Over):
        #temp用于记录是否是当日的代理IP,如果不是记录其位置
        temp=-1

        url1=url.format(num=_num)
        html=GPI.GetHtmlpage(url1)
        result=GPI.cleanHtml(html)



        for k in range(len(result[5])):
            if result[5][k]!=currentTime:
                temp=k
                Is_Over=False
                break
        #如果temp=-1，就全部进行写入
        if temp==-1:
            for i in range(len(result)):
                for j in range(len(result[i])):
                    print("yi写入"+str(result[i][j]))
                    sheet.write(index+j+1,i,result[i][j])
        else:
            for k in range(len(result)):
                for kk in range(temp):
                    print("yi写入" + str(result[k][kk]))
                    sheet.write(index+kk+1,k,  result[k][kk])
        _num += 1
        index+=len(result[0])
        time.sleep(16)
    #
    print("写入完成")
    book.save("proxy.xls")