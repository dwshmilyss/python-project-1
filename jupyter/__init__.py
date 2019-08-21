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
@time: 2017/8/9 14:04
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
    print(sys.getsizeof(u""))
    print(sys.getsizeof(u"a"))
    print(sys.getsizeof(u"b"))
    print(u"a".__sizeof__())
    print(u"b".__sizeof__())
    print(sys.getsizeof(b""))
    print(sys.getsizeof(b"a"))
    print(sys.getsizeof(b"b"))
    pass