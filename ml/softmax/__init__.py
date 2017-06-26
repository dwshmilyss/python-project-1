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
@time: 2017/6/26 下午5:18 
"""

import sys

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
    pass