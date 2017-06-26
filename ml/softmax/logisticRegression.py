#!/usr/bin/env python 
# encoding: utf-8 


""" 
@version: v1.0 
@author: duanwei 
@license: Apache Licence 
@contact: 4064865@qq.com 
@site: http://blog.csdn.net/dwshmilyss 
@software: PyCharm 
@file: logisticRegression.py 
@time: 2017/6/26 下午5:28 
"""

import cPickle
import gzip
import os
import sys
import time

import numpy

import theano
import theano.tensor as T

default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def func():
    pass


# 参数说明：
# input，输入的一个batch，假设一个batch有n个样本(n_example)，则input大小就是(n_example,n_in)
# n_in,每一个样本的大小，MNIST每个样本是一张28*28的图片，故n_in=784
# n_out,输出的类别数，MNIST有0～9共10个类别，n_out=10
class LogisticRegression(object):
    def __init__(self, input, n_in, n_out):
        # W大小是n_in行n_out列，b为n_out维向量。即：每个输出对应W的一列以及b的一个元素。WX+b
        # W和b都定义为theano.shared类型，这个是为了程序能在GPU上跑。
        self.W = theano.shared(
            value=numpy.zeros((n_in, n_out), dtype=theano.config.floatX),
            name='W',
            borrow=True)

        self.b = theano.shared(
            value=numpy.zeros((n_out,),dtype=theano.config.floatX),
            name='b',
            borrow=True
        )

        # input是(n_example,n_in)，W是（n_in,n_out）,点乘得到(n_example,n_out)，加上偏置b，
        # 再作为T.nnet.softmax的输入，得到p_y_given_x
        # 故p_y_given_x每一行代表每一个样本被估计为各类别的概率
        # PS：b是n_out维向量，与(n_example,n_out)矩阵相加，内部其实是先复制n_example个b，
        # 然后(n_example,n_out)矩阵的每一行都加b
        self.p_y_given_x = T.nnet.softmax(T.dot(input, self.W) + self.b)

        #argmax返回最大值下标，因为本例数据集是MNIST，下标刚好就是类别。axis=1表示按行操作。
        self.y_pred = T.argmax(self.p_y_given_x, axis=1)

        #params，模型的参数
        self.params = [self.W, self.b]

    # 代价函数NLL
    # 因为我们是MSGD，每次训练一个batch，一个batch有n_example个样本，则y大小是(n_example,),
    # y.shape[0]得出行数即样本数，将T.log(self.p_y_given_x)简记为LP，
    # 则LP[T.arange(y.shape[0]),y]得到[LP[0,y[0]], LP[1,y[1]], LP[2,y[2]], ...,LP[n-1,y[n-1]]]
    # 最后求均值mean，也就是说，minibatch的SGD，是计算出batch里所有样本的NLL的平均值，作为它的cost
    def negative_log_likelihood(self, y):
        return -T.mean(T.log(self.p_y_given_x)[T.arange(y.shape[0]), y])

    # batch的误差率
    def errors(self, y):
        # 首先检查y与y_pred的维度是否一样，即是否含有相等的样本数
        if y.ndim != self.y_pred.ndim:
            raise TypeError(
                'y should have the same shape as self.y_pred',
                ('y', y.type, 'y_pred', self.y_pred.type)
            )
            # 再检查是不是int类型，是的话计算T.neq(self.y_pred, y)的均值，作为误差率
        # 举个例子，假如self.y_pred=[3,2,3,2,3,2],而实际上y=[3,4,3,4,3,4]
        # 则T.neq(self.y_pred, y)=[0,1,0,1,0,1],1表示不等，0表示相等
        # 故T.mean(T.neq(self.y_pred, y))=T.mean([0,1,0,1,0,1])=0.5，即错误率50%
        if y.dtype.startswith('int'):
            return T.mean(T.neq(self.y_pred, y))
        else:
            raise NotImplementedError()

if __name__ == "__main__":
    print T.arange(1,10,1,'int64')
    print theano.__version__
    pass
