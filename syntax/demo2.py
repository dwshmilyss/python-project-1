#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: Lieb
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: demo2.py
@time: 2017/3/31 10:22
"""

import socket
import sys
import re

class Main():
    def __init__(self):
        pass

import contextlib
@contextlib.contextmanager
def socketcontext(*args, **kw):
    s = socket(*args, **kw)
    try:
        yield s
    finally:
        s.close()

# with socketcontext(socket.AF_INET, socket.SOCK_STREAM) as s:
#     # 1. 与服务器建立连接
#     s.connect(("www.seriot.ch", 80))
#     # 2. 构建请求行，请求资源是 index.php
#     request_line = b"GET /index.php HTTP/1.1"
#     # 3. 构建请求首部，指定主机名
#     headers = b"Host: seriot.ch"
#     # 4. 用空行标记请求首部的结束位置
#     blank_line = b"\r\n"
#
#     # 请求行、首部、空行这3部分内容用换行符分隔，组成一个请求报文字符串
#     # 发送给服务器
#     message = b"\r\n".join([request_line, headers, blank_line])
#     print message
#     s.send(message)
#
#     # 服务器返回的响应内容稍后进行分析
#     response = s.recv(1024)
#     print response

from contextlib import closing
def test_socket():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        # 1. 与服务器建立连接
        s.connect(("www.seriot.ch", 80))
        # 2. 构建请求行，请求资源是 index.php
        request_line = b"GET /index.php HTTP/1.1"
        # 3. 构建请求首部，指定主机名
        headers = b"Host: seriot.ch"
        # 4. 用空行标记请求首部的结束位置
        blank_line = b"\r\n"

        # 请求行、首部、空行这3部分内容用换行符分隔，组成一个请求报文字符串
        # 发送给服务器
        message = b"\r\n".join([request_line, headers, blank_line])
        print message
        s.send(message)

        # 服务器返回的响应内容稍后进行分析
        response = s.recv(1024)
        print response


if __name__ == "__main__":
    test_socket()
    pass