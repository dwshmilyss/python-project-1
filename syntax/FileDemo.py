#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: Lieb
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: FileDemo.py
@time: 2017/4/1 18:16
"""


def del_dir_tree(path):
    ''' 递归删除目录及其子目录,　子文件'''
    if os.path.isfile(path):
        try:
            os.remove(path)
        except Exception, e:
            #pass
            print e
    elif os.path.isdir(path):
        for item in os.listdir(path):
            itempath = os.path.join(path, item)
            del_dir_tree(itempath)
        try:
            os.rmdir(path)   # 删除空目录
        except Exception, e:
            #pass
            print e


class Main():
    def __init__(self):
        pass


if __name__ == "__main__":
    # fo = open("foo.txt", "wb")
    # fo.write("www.runoob.com!\nVery good site!\n");
    #
    # # 关闭打开的文件
    # fo.close()

    # 打开一个文件
    fo = open("foo.txt", "r+")
    str = fo.read(10);
    print "读取的字符串是 : ", str

    # 查找当前位置
    position = fo.tell();
    print "当前文件位置 : ", position

    # 把指针再次重新定位到文件开头
    position = fo.seek(0, 0);
    str = fo.read(10);
    print "重新读取字符串 : ", str
    # 关闭打开的文件
    fo.close()

    import os
    from os import path

    # 给出当前的目录
    print os.getcwd()
    # os.makedirs("")
    # os.mkdir("aaa/aa/a")
    os.makedirs("aaa/aa/a")
    # del_dir_tree("aaa")
    pass