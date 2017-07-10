#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: cPickle_demo.py
@time: 2017/6/27 17:22
"""

'''
很有必要在程序中加入定时保存参数的功能，这样下次训练就可以将参数初始化为上次保存下来的结果，而不是从头开始随机初始化。
调用cPickle持久化数据
python里有 cPickle 和 pickle ，cPickle基于c实现，比pickle快。
'''
def test1():
    a = [1, 2, 3]
    b = {4: 5, 6: 7}
    # 保存，cPickle.dump函数。/home/wepon/ab是路径，ab是保存的文件的名字，如果/home/wepon/下本来就有ab这个文件，将被覆写#，如果没有，则创建。'wb'表示以二进制可写的方式打开。dump中的-1表示使用highest protocol。
    import cPickle

    write_file = open('d:/ab', 'wb')
    cPickle.dump(a, write_file, -1)
    cPickle.dump(b, write_file, -1)
    write_file.close()

    # 读取，cPickle.load函数。
    read_file = open('d:/ab', 'rb')
    a_1 = cPickle.load(read_file)
    b_1 = cPickle.load(read_file)
    print a, b
    read_file.close()


class Main():
    def __init__(self):
        pass


if __name__ == "__main__":
    pass