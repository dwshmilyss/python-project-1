#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: Lieb
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: loggingDemo.py
@time: 2017/4/1 17:18
默认情况下，logging将日志打印到屏幕，日志级别为WARNING；
日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET，当然也可以自己定义日志级别。
"""


import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')


#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################

from sklearn.datasets import load_iris
from numpy import vstack, array, nan
if __name__ == "__main__":
    logging.debug('This is debug message')
    logging.info('This is info message')
    logging.warning('This is warning message')
    iris = load_iris()
    from sklearn.feature_selection import SelectKBest
    from scipy.stats import pearsonr

    print "利用相关系数法过滤后的前5个样本的特征："
    print "=========================="
    # print (SelectKBest(lambda X, Y: array(map(lambda x:pearsonr(x, Y), X.T)).T, k=2).fit(iris.data,iris.target)[0:5])
    # a = SelectKBest(lambda X, Y: array(map(lambda x: pearsonr(x, Y), X.T)).T, k=2)
    # print a.fit_transform(iris.data, iris.target)
    from sklearn.feature_selection import chi2
    b = SelectKBest(chi2, k=2).fit_transform(iris.data, iris.target)
    print "=========================="
    pass