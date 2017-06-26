#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: Lieb
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: __init__.py.py
@time: 2017/4/10 15:05
"""
import os
import sys

# sys.path.append("../")
projectPath = os.path.abspath(os.path.dirname(sys.argv[0]))
from NLP.baseOnDict import textprocessing as tp
import numpy as np


def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == "__main__":
    HTCPath = projectPath + "/test_dataset/HTC Z710t_review_2013.6.5.xlsx"
    HTCData = tp.get_excel_data(HTCPath, 1, 1, "data")
    arr = [(1,2),(2,2),(3,2)]
    np_arr = np.array(arr)
    print np.sum(np_arr[:,0])
    print np.mean(np_arr[:,0])
    print np.std(np_arr[:,0])
    pass