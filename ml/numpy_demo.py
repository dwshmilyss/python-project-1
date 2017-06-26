#!/usr/bin/env python 
# encoding: utf-8 


""" 
@version: v1.0 
@author: duanwei 
@license: Apache Licence 
@contact: 4064865@qq.com 
@site: http://blog.csdn.net/dwshmilyss 
@software: PyCharm 
@file: numpy_demo.py 
@time: 2017/6/26 上午11:49 
"""

import sys
import numpy as np

default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)




def func():

    pass


class Main():
    def __init__(self):
        pass


if __name__ == "__main__":
    a = np.random.random(10)
    print a
    a.sort()
    pass