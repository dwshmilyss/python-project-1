#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: kmeans.py
@time: 2017/7/20 15:39
"""
from numpy import *
import time
import matplotlib.pyplot as plt
import ml.log

import sys
default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def func():
    pass


class Kmeans():
    def __init__(self):
        pass

    #计算2个向量的距离(欧几里得距离)
    def euclDistance(self,vector1,vector2):
        return sqrt(sum(power(vector2-vector1,2)))

    #随机从数据集中选择k个质心
    def initCentroids(self,dataSet,k):
        numSamples,dim = dataSet.shape
        #初始化一个零矩阵
        centroids = zeros((k,dim))
        for i in range(k):
            '''
              随机抽样(随机抽取k个样本点) 
              numpy.random.uniform(low,high,size)
            '''
            index = int(random.uniform(0,numSamples))
            #用随机抽到的样本点初始化质心
            centroids[i,:] = dataSet[index,:]
        return centroids

    #kmeans cluster
    def kmeans(self,dataSet,k):
        #获取数据集的行数
        numSamples = dataSet.shape[0]
        #初始化一个和样本矩阵相同维度的0矩阵
        clusterAssment = mat(zeros((numSamples, 2)))
        clusterChanged = True

        ## step 1: init centroids 初始化k个质心
        centroids = self.initCentroids(dataSet, k)

        while clusterChanged:
            clusterChanged = False
            ## for each sample 遍历每一个样本点
            for i in xrange(numSamples):
                minDist = 100000.0
                minIndex = 0
                ## for each centroid
                ## step 2: find the centroid who is closest #计算该样本点和每一个质心的欧几里德距离
                ## 这个循环完成后，假如说找到第5个质心离该样本最近，则minDist被更新该样本距离该质心的距离，minIndex被更新成5
                for j in range(k):
                    distance = self.euclDistance(centroids[j, :], dataSet[i, :])
                    #获取和该样本点最小距离的那个质心 同时更新最小距离 最小距离的质心
                    if distance < minDist:
                        minDist = distance
                        minIndex = j

                        ## step 3: update its cluster
                if clusterAssment[i, 0] != minIndex:
                    clusterChanged = True
                    clusterAssment[i, :] = minIndex, minDist ** 2

            ## step 4: update centroids 更新质心（求均值）
            ## clusterAssment[:, 0] 获取矩阵的第一列
            ## clusterAssment[:, 0].A 由类型matrix转换为ndarray
            ## nonzero(clusterAssment[:, 0].A == j) 然后获取第一列中等于j的元素的下标 返回2个数组，第一个数组是元素的下标 第二个数组还不知道是啥
            ## 这一步走完等于说每一个k值都成为一个簇
            ## centroids[j, :] = mean(pointsInCluster, axis=0) 对该簇求新的质心（均值）
            for j in range(k):
                pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]
                centroids[j, :] = mean(pointsInCluster, axis=0)

        print 'Congratulations, cluster complete!'
        return centroids, clusterAssment

    # show your cluster only available with 2-D data
    def showCluster(self,dataSet, k, centroids, clusterAssment):
        numSamples, dim = dataSet.shape
        if dim != 2:
            print "Sorry! I can not draw because the dimension of your data is not 2!"
            return 1

        mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
        if k > len(mark):
            print "Sorry! Your k is too large! please contact Zouxy"
            return 1

            # draw all samples
        for i in xrange(numSamples):
            markIndex = int(clusterAssment[i, 0])
            plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

        mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
        # draw the centroids
        for i in range(k):
            plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)

        plt.show()

if __name__ == "__main__":
    ## step 1: load data
    print "step 1: load data..."
    dataSet = []
    fileIn = open('testSet.txt')
    for line in fileIn.readlines():
        lineArr = line.strip().split('\t')
        dataSet.append([float(lineArr[0]), float(lineArr[1])])

    ## step 2: clustering...
    print "step 2: clustering..."
    dataSet = mat(dataSet)
    k = 4
    kmeansInstance = Kmeans()
    centroids, clusterAssment = kmeansInstance.kmeans(dataSet, k)

    ## step 3: show the result
    print "step 3: show the result..."
    kmeansInstance.showCluster(dataSet, k, centroids, clusterAssment)
    pass