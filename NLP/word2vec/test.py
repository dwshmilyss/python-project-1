#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: test.py
@time: 2017/6/19 16:18
"""

from SolrUtil import MySolrPy

# 连接数据库
msp = MySolrPy('http://localhost:8080/solr/test')
msp.delAll()
# for i in range(1,105):
#     bean = {
#         'id': i,
#         'content': u"哈哈哈",
#     }
#     msp.add(bean)
#
# msp.commit()

print 'ok'