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
            index = int(random.uniform(0,numSamples))
            centroids[i,:] = dataSet[index,:]
        return centroids

    #kmeans cluster
    def kmeans(self,dataSet,k):
        #获取数据集的行数
        numSamples = dataSet.shape[0]
        clusterAssment = mat(zeros((numSamples, 2)))
        clusterChanged = True

        ## step 1: init centroids
        centroids = self.initCentroids(dataSet, k)

        while clusterChanged:
            clusterChanged = False
            ## for each sample
            for i in xrange(numSamples):
                minDist = 100000.0
                minIndex = 0
                ## for each centroid
                ## step 2: find the centroid who is closest
                for j in range(k):
                    distance = self.euclDistance(centroids[j, :], dataSet[i, :])
                    if distance < minDist:
                        minDist = distance
                        minIndex = j

                        ## step 3: update its cluster
                if clusterAssment[i, 0] != minIndex:
                    clusterChanged = True
                    clusterAssment[i, :] = minIndex, minDist ** 2

                    ## step 4: update centroids
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