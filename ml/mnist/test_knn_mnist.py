#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: test_knn_mnist.py
@time: 2017/6/27 10:52
"""

from sklearn import neighbors
from data_util import DataUtils
import datetime
import sys


def main():
    trainfile_X = 'D:/10000347/Downloads/machine_learning/data/mnist/train-images-idx3-ubyte.gz'
    trainfile_y = 'D:/10000347/Downloads/machine_learning/data/mnist/train-labels-idx1-ubyte.gz'
    testfile_X = 'D:/10000347/Downloads/machine_learning/data/mnist/t10k-images-idx3-ubyte.gz'
    testfile_y = 'D:/10000347/Downloads/machine_learning/data/mnist/t10k-labels-idx1-ubyte.gz'
    train_X = DataUtils(filename=trainfile_X).getImage()
    train_y = DataUtils(filename=trainfile_y).getLabel()
    test_X = DataUtils(testfile_X).getImage()
    test_y = DataUtils(testfile_y).getLabel()

    return train_X, train_y, test_X, test_y


def testKNN():
    train_X, train_y, test_X, test_y = main()
    startTime = datetime.datetime.now()
    knn = neighbors.KNeighborsClassifier(n_neighbors=3)
    knn.fit(train_X, train_y)
    match = 0;
    for i in xrange(len(test_y)):
        predictLabel = knn.predict(test_X[i])[0]
        if (predictLabel == test_y[i]):
            match += 1

    endTime = datetime.datetime.now()
    print 'use time: ' + str(endTime - startTime)
    print 'error rate: ' + str(1 - (match * 1.0 / len(test_y)))


if __name__ == "__main__":
    print sys.maxint
    for i in range(sys.maxint):
        pass
    # 2055376946
    # testKNN()