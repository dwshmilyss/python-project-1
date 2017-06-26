#!/usr/bin/env python
# encoding: utf-8

import jieba
import jieba.posseg
jieba.initialize()
import sys
import os
import site
# sys.path.appe
import platform

default_encoding="utf-8"
if(default_encoding!=sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import os

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../../log/NLP_demo1.log',
                filemode='w')

#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################



sysstr = platform.system()
python27PackagePath = ''
if(sysstr =="Windows"):
    python27PackagePath = os.path.abspath(site.getsitepackages()[-1])
elif(sysstr == "Linux"):
    python27PackagePath = os.path.abspath(site.getsitepackages()[0])
else:
    print ("Other System tasks")
jiebaPath = python27PackagePath + "/jieba"

#Load user dictionary to increse segmentation accuracy
jieba.load_userdict(jiebaPath + "/userdict.txt")

stopWords = [line.strip().decode('utf-8') for line in open(jiebaPath + "/stopword.txt").readlines()]

"""
@version: v1.0
@author: Lieb
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: demo1.py
@time: 2017/4/19 14:25
"""

def segmentation(sentence, para):
    # 返回一个字符串
    seg_list = jieba.cut(sentence)
    if para == 'str':
        seg_result = ' '.join([word for word in seg_list if word not in stopWords and word != ' '])
        return seg_result
    # 返回一个list
    elif para == 'list':
        seg_result2 = [word for word in seg_list if word not in stopWords and word != ' ']
        return seg_result2


def process_file_data(inPath,outPath):
    try:
        inputFile = open(inPath,"r")
        lines = inputFile.readlines()
        outFile = open(outPath, 'w')
        print lines.__len__()
        for line in lines:
            print line
            temp = line.decode("utf8").strip("\n").rstrip("</content>").lstrip("<content>")
            print temp
            cut = segmentation(temp,'str')
            print cut
            # outFile.write(cut.strip() + "\n")
        outFile.close()
        inputFile.close()
    except IOError as err:  # 使用as将异常对象，并将其赋值给一个标识符
        print('File Error:' + str(err))
    finally:
        if 'inputFile' in locals():
            inputFile.close()
        if 'outFile' in locals():
            outFile.close()



class Main():
    def __init__(self):
        pass



if __name__ == "__main__":
    str = "<content></content>"
    str1 = str.rstrip("</content>").lstrip("<content>")
    if str1 and str1 != '':
        print 'str1 is not empty'
    else:
        print 'str1 is empty'
    # logging.info("begin....")
    # process_file_data(sys.argv[1],sys.argv[2])
    # process_file_data('test.txt','test_out.txt')
    # logging.info("end....")
    pass