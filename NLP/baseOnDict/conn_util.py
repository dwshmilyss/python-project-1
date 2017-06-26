#!/usr/bin/env python
# encoding: utf-8
import log
import MySQLdb
import traceback

"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: conn.py
@time: 2017/6/6 12:18
"""


def createConn():
    try:
        conn = MySQLdb.connect(
            host='10.21.3.120',
            port=3306,
            user='root',
            passwd='wenha0',
            db='test',
        )
        cur = conn.cursor()
        conn.set_character_set('utf8')
        cur.execute('SET NAMES utf8mb4;')
        cur.execute('SET CHARACTER SET utf8mb4;')
        cur.execute('SET character_set_connection=utf8mb4;')
    except Exception as e:
        log.logger.error("create mysql conn error : " + traceback.format_exc())
    return (conn, cur)


def closeConn(conn,cur):
    try:
        # 释放数据连接
        if cur:
            cur.close()
        if conn:
            conn.close()
    except Exception as e:
        log.logger.error("close mysql conn error : " + traceback.format_exc())

class Main():
    def __init__(self):
        pass


if __name__ == "__main__":
    pass
