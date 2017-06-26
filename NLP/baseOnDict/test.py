#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: dww
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: test.py.py
@time: 2017/4/10 15:22
"""
import jieba
jieba.initialize()
import xlrd
import sys
import os
# sys.path.append("../")
import jieba.posseg as pseg
projectPath = os.path.abspath(os.path.dirname(sys.argv[0]))
python27PackagePath = os.path.abspath(sys.path[sys.path.__len__()-1])
jiebaPath = python27PackagePath + "/jieba"

stopWords=[line.strip().decode('utf-8') for line in open(jiebaPath + "/stopword_test.txt").readlines()]

def test_jieba():
    # seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
    # print "Full Mode:", "/ ".join(seg_list)  # 全模式
    # seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
    # print "Default Mode:", "/ ".join(seg_list)  # 精确模式
    # seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
    # print ", ".join(seg_list)
    # seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    # print ", ".join(seg_list)
    # test_sent = "李小福是创新办主任也是云计算方面的专家;"
    test_sent = "除了电池不给力，都很好"
    words = jieba.cut(test_sent)
    data = []
    for word in words:
        data.append(word)
    print "use userdict before : " + " / ".join(data)
    # # jieba.load_userdict(jiebaPath + "\\userdict_test.txt")
    # # res = [word for word in words if word not in stopWords]
    res = [word for word in data if word not in stopWords and word != ' ']
    print "use userdict after : " + " / ".join(res)
    # pass

import numpy as np
import math
if __name__ == "__main__":
    # test_jieba()
    # print "abcd"[::-1]
    # alist = [1,2,3,4]
    # alist.extend([5, 6, 7, 8])
    # print len(alist)
    # a = 1.4
    # # 向下取整
    # print math.floor(a)
    # # 向上取整
    # print math.ceil(a)
    # # 四舍五入
    # print round(a)
    # # 直接去掉小数部分
    # print int(a)
    print locals()
    pass