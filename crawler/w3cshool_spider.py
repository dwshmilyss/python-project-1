#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: Lieb
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: w3cshool_spider.py
@time: 2017/4/1 15:32
"""
'''
1. logging.CRITICAL - for critical errors (highest severity) 致命错误
2. logging.ERROR - for regular errors 一般错误
3. logging.WARNING - for warning messages 警告＋错误
4. logging.INFO - for informational messages 消息＋警告＋错误
5. logging.DEBUG - for debugging messages (lowest severity) 低级别
'''
# logging.error("This is a warning")

# logging.log(logging.INFO,"This is a warning")



if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('SimilarFace').addHandler(console)
    #获取实例对象
    # logger=logging.getLogger()
    # logger.warning("这是警告消息")
    #指定消息发出者

    logging.info('aaa')
    # logger.error("This is a warning")
    # # 方法2 自己定义个logger
    # a = "ddd"
    # logger.info('Parse function called on a')
    pass