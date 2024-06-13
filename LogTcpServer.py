# -*- coding: utf-8 -*-  


import json
import errno
import socket
import thread
import urllib2
import threading
import SocketServer
from string import join
from time import sleep, ctime
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

HOST = ''
PORT = 5457
ADDR = (HOST, PORT)

idx = 0
recv_buff = []

# 创建TCP服务器
class requestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        print 'connected from:', self.client_address[0] + ':' + str(self.client_address[1])

    # 判断是否是json
    def is_json(self, jtxt):
        try:
            json.loads(jtxt)
        except ValueError, e:
            return False
        return True

    def handle(self):
        global idx
        global recv_buff
        whole = ""
        while True:
            try:
                # 接收数据
                data = self.request.recv(1024).strip()
                if not data: break
                whole += data
                begin = 0
                above = 50
                pos   = 51
                while pos > above:
                    pos = whole.find('}', pos)+1
                    if pos > 0 and self.is_json(whole[begin:pos]):
                        recv_buff.append(whole[begin:pos])
                        print '[', whole[begin:pos],']'
                        idx = idx + 1
                        print 'idx = ',idx
                        begin = pos
                whole = whole[begin:]

                # 如果数量超过100条，调用 孙正华 接口 把 100条消息全部发送
                if idx >= 100:
                    print 'flush buffer'
                    idx = 0
                    flushBuffer()
            # except SocketError as e:
            except:
                print 'except'
                # print 'error',e.errno,errno.ECONNRESET
                # if e.errno != errno.ECONNRESET:
                #   raise
                # pass
                # traceback.print_exc()
                self.request.close()  
                break
    def finish(self):
        print 'client:', self.client_address[0] + ':' + str(self.client_address[1]), 'disconnect.'
        self.request.close()

# 清空缓存区，调用接口发送缓存中的消息
def flushBuffer():
    global recv_buff
    send_data = join(recv_buff, ',')
    # print send_data
    send_data = '[[' + send_data + ']]'
    if send_data == '[[]]':
        return
    # 调用接口
    sendHttpRequest('Logger', 'sysLogger', send_data)
    recv_buff = []


# 30秒后自动调用接口
def delayFlush(): 
    while True:
        sleep(30)
        print 'flush buffer by delay'
        flushBuffer()

# 发送HTTP请求
def sendHttpRequest(module, func, data):
    register_openers()
    url = 'http://service.1.logger'
    params = {}
    params['clientID'] = 'yiban.cn'
    params['passwd'] = '7622f0d078cf468395336320c3cf35a1'    
    params['module'] = module
    params['func'] = func
    params['args'] = data
    params['abc'] = 1
    data, headers = multipart_encode(params)
    print "data is",data
    # print "headers is",headers
    request = urllib2.Request(url, data, headers)
    print "request is ",urllib2.urlopen(request)

if __name__ == '__main__':
    try:
        print 'listen port: ' + str(PORT)
        tcpServ = SocketServer.ThreadingTCPServer(ADDR, requestHandler)
        print 'waiting for connection.'
        thread.start_new_thread(delayFlush, ())
        tcpServ.serve_forever()
    except KeyboardInterrupt:
        print "server has been closed."
        tcpServ.shutdown()
        quit()


