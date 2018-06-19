#!/usr/bin/env python
# encoding: utf-8

from numpy import *
import operator
from os import listdir
import matplotlib.pyplot as plt

'''
fileName 数据集文件名
numberOfFeature 特征个数
'''
def getDataSet(fileName,numberOfFeature):
    fr = open(fileName)
    cn = len(fr.readlines())
    mat = zeros((cn,numberOfFeature))
    labelVector = []
    idx = 0
    fr = open(fileName)
    for line in fr.readlines():
        line = line.strip()
        temp = line.split(",")
        #list类型这样操作错误
        mat[idx,:] = temp[0:numberOfFeature]
        if temp[-1] == "Iris-setosa":
            labelVector.append(1)
        elif temp[-1] == "Iris-versicolor":
            labelVector.append(2)
        elif temp[-1] == "Iris-virginica":
            labelVector.append(3)
        else:
            labelVector.append(4)
        idx += 1
    return mat,labelVector

'''
切分数据集
# 鸢尾花数据集共三类，每类50个数据，50（35训练集 / 15测试集）
'''
def dataDiv(inMat,classVector):
    trainData = []
    trainLabel = []
    testData = []
    testLabel = []

    for i in range(0,35):
        #每一类训练集取35个 数据集中的每个类别刚好都是排列在一起的 所以按下标获取就可以
        trainData.append(inMat[i,:])
        trainData.append(inMat[i+50,:])
        trainData.append(inMat[i+100,:])

        trainLabel.append(classVector[i])
        trainLabel.append(classVector[i+50])
        trainLabel.append(classVector[i+100])

    for i in range(35,50):
        testData.append(inMat[i,:])
        testData.append(inMat[i+50,:])
        testData.append(inMat[i+100,:])

        testLabel.append(classVector[i])
        testLabel.append(classVector[i+50])
        testLabel.append(classVector[i+100])

    return trainData,trainLabel,testData,testLabel


#定义sigmoid函数
def sigmoid(inX):
    return 1.0 / (1+exp(-inX))

#梯度上升求最优解(因为是极大对数似然函数估计 所以求的是最大值)
def gradAscent(dataMat,labelMat,alpha,epochs):
    dataMatrix = mat(dataMat)
    classLabel = mat(labelMat).transpose()
    m,n = shape(dataMatrix)
    beta = ones((n,1))
    for i in range(epochs):
        y = sigmoid(dot(dataMatrix,beta))
        loss = classLabel - y #计算残差
        #更新参数
        beta = beta + alpha * dataMatrix.transpose()*loss
    return beta

def plotBestFit(weights,dataMat,labelMat):  #画出最终分类的图
    import matplotlib.pyplot as plt
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()



if __name__ == "__main__":
    # load_data('D:/10000347/Downloads/machine_learning/data/mnist/mnist.pkl.gz');
    # sgd_optimization_mnist(dataset='D:/10000347/Downloads/machine_learning/data/mnist/mnist.pkl.gz')
    dataMat, labelMat = getDataSet('../../data/iris/iris.data', 4)
    alpha = 0.01
    epochs = 500
    trainData, trainLabel, testData, testLabel = dataDiv(dataMat, labelMat)
    DD = dataMat[:,(1,3)]
    print DD
    X = [x[0] for x in DD]
    Y = [x[1] for x in DD]

    # plt.scatter(X, Y, c=iris.target, marker='x')
    plt.scatter(X[:50], Y[:50], color='red', marker='o', label='setosa')  # 前50个样本
    plt.scatter(X[50:100], Y[50:100], color='blue', marker='x', label='versicolor')  # 中间50个
    plt.scatter(X[100:], Y[100:], color='green', marker='+', label='Virginica')  # 后50个样本
    plt.legend(loc=2)  # 左上角
    plt.show()
    # # 将numpy矩阵转换为数组
    # weights = gradAscent(dataMat, labelMat, alpha, epochs).getA()
    # print weights
    # plotBestFit(weights,trainData,trainLabel)