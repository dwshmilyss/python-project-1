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

# 定义空列表，用于创建所有的爬虫链接
urls = []
# 指定爬虫所需的上海各个区域名称
citys = ['pudongxinqu', 'minhang', 'baoshan', 'xuhui', 'putuo', 'yangpu', 'changning', 'songjiang',
         'jiading', 'huangpu', 'jinan', 'zhabei', 'hongkou', 'qingpu', 'fengxian', 'jinshan', 'chongming']

# 基于for循环，构造完整的爬虫链接
# for i in citys:
#     url = 'http://sh.lianjia.com/ershoufang/%s/' % i
#     res = requests.get(url)  # 发送get请求
#     res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则会有问题
#     soup = BeautifulSoup(res, 'html.parser')  # 使用bs4模块，对响应的链接源代码进行html解析
#     # page = soup.findAll('div', {'class': 'page-box house-lst-page-box'})  # 使用finalAll方法，获取指定标签和属性下的内容
#     page = soup.findAll('div', {'class': 'c-pagination'})  # 使用finalAll方法，获取指定标签和属性下的内容
#     pages = [i.strip() for i in page[0].text.split('\n')]  # 抓取出每个区域的二手房链接中所有的页数
#     if len(pages) > 3:
#         total_pages = int(pages[-3])
#     else:
#         total_pages = int(pages[-2])
#
#     for j in list(range(1, total_pages + 1)):  # 拼接所有需要爬虫的链接
#         urls.append('http://sh.lianjia.com/ershoufang/%s/d%s' % (i, j))

for i in range(1,2909):
    urls.append('http://sh.lianjia.com/ershoufang/d%s' % i)

from io import open
# 创建csv文件，用于后面的保存数据
file = open('lianjia.csv', 'w',encoding='utf-8')

for url in urls:  # 基于for循环，抓取出所有满足条件的标签和属性列表，存放在find_all中
    print url
    res = requests.get(url)
    res = res.text.encode(res.encoding).decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    find_all = soup.select('#js-ershoufangList > div.content-wrapper > div.content > div.m-list > ul > li')
    print len(find_all)
    for i in range(len(find_all)):  # 基于for循环，抓取出所需的各个字段信息
        res2 = find_all[i]
        title = res2.find(name='a', attrs={'class': 'text link-hover-green js_triggerGray js_fanglist_title'})[
            'title']  # 每套二手房的标语
        xiaoqu_name = res2.find(name='a', attrs={'class': 'laisuzhou'}).find('span').string  # 每套二手房的小区名称
        region_1 = res2.find(name='span', attrs={'class': 'info-col row2-text'}).find(
            'a').find_next().find_next().string  # 属于哪个区
        region_2 = res2.find(name='span', attrs={'class': 'info-col row2-text'}).find(
            'a').find_next().find_next().find_next().string  # 属于哪个区的二级地区
        try:
            build_year = res2.find(name='span', attrs={'class': 'info-col row2-text'}).text.strip().split('|')[3].strip()  # 建造年份
        except Exception as e:
            continue
        unit_price_temp = res2.find('span', {'class': 'info-col price-item minor'}).text.strip()  # 单价
        unit_price = unit_price_temp[2:unit_price_temp.find(u'元')]

        total_price = res2.find('span', {'class': 'total-price strong-num'}).text  # 总价

        temp = res2.find('span', {'class': 'info-col row1-text'}).text

        try:
            # 采用列表解析式，删除字符串的首位空格
            info = [i.strip() for i in temp.strip().split('|')]
            house_type = info[0].replace(' ','')  # 房型
            house_area = info[1]  # 面积
            hosue_floor = info[2]  # 楼层
            house_direction = info[3]  # 朝向
        except Exception as e:
            continue

        # print(name,room_type,size,region,loucheng,chaoxiang,price,price_union,builtdate)
        # 将上面的各字段信息值写入并保存到csv文件中
        str = ' '.join(
            [xiaoqu_name, house_type, house_area, region_1, region_2, hosue_floor, house_direction, total_price,
             unit_price,
             build_year, title]) + '\n'
        print str
        file.write(str)  # 关闭文件（否则数据不会写入到csv文件中）
file.close()
