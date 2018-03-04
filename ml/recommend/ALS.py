#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: ALS.py
@time: 2018/1/31 10:31
"""
from numpy import *
import numpy as np
import sys
from pylab import *

import implicit_mf

default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def func():
    pass


class Main():
    def __init__(self):
        pass


'''
最小交替二乘法
这个方法有问题，得到的结果矩阵和梯度下降法得到的矩阵有明显差别，而且这个还会得到负值
有待进一步查明原因
R为m*n的原始评分矩阵
P为m*k的低秩矩阵
Q为n*k的低秩矩阵
'''


def als(R, K, steps=5000, beta=0.01):
    m, n = np.shape(R)
    P = np.mat(np.random.rand(m, K))
    Q = np.mat(np.random.rand(n, K))
    for step in xrange(steps):
        # for i in xrange(m):
        #     for j in xrange(n):
        #         if R[i, j] > 0:
        #             # 把P固定，更新Q
        #             temp = (np.dot(P.T, P) + beta * np.eye(K)).I
        #             temp1 = temp * P.T * R[:, j]
        #             Q[j, :] = temp1.T
        #     # Q固定 更新P
        #     P[i, :] = ((np.dot(Q.T, Q) + beta * np.eye(K)).I * Q.T * R[i, :].T).T
        for j in xrange(n):
            # 把P固定，更新Q
            temp = (np.dot(P.T, P) + beta * np.eye(K)).I
            temp1 = temp * P.T * R[:, j]
            Q[j, :] = temp1.T
        for i in xrange(m):
            # Q固定 更新P
            P[i, :] = ((np.dot(Q.T, Q) + beta * np.eye(K)).I * Q.T * R[i, :].T).T
        eR = np.dot(P, Q.T)
        e = 0
        cn = 0
        sum = 0
        for i in xrange(m):
            for j in xrange(n):
                if R[i, j] > 0:
                    sum += pow((R[i, j] - eR[i, j]), 2)
                    cn += 1
                    pass
        e = sqrt(sum / cn)
        if e < 0.001:
            print 'loss:%f' % e
            break
        if step % 1000 == 0:
            print 'loss:%f' % e
    return P, Q


'''
加载一个矩阵评分数据
'''


def load_data(path):
    f = open(path)
    data = []
    for line in f.readlines():
        arr = []
        lines = line.strip().split("\t")
        for x in lines:
            if x != "-":
                arr.append(float(x))
            else:
                arr.append(float(0))
        # print arr
        data.append(arr)
    # print data
    return data


'''
梯度下降法
'''


def gradient_descent(R, K, maxEpoches=10000, alpha=0.001, beta=0.01):
    m = len(R)  # 用户数目
    n = len(R[0])  # 物品数目
    K = 2
    # 随机生成一个m*K的矩阵(user)
    U = np.random.rand(m, K)
    # 随机生成一个K*n的矩阵(item)
    V = np.random.rand(n, K)
    # 转置物品矩阵
    V = V.T
    # 开始迭代
    for step in xrange(maxEpoches):
        for i in xrange(m):
            for j in xrange(n):
                if math.fabs(R[i][j]) > 1e-4:  # 只预测非0元素
                    # 定义当前误差
                    # 原始评分矩阵的第i行第j列的值 - u的第i行*v的第j列
                    error_i_j = R[i][j] - np.dot(U[i, :], V[:, j])
                    # 求出梯度后更新 u,v
                    for k in xrange(K):
                        U[i][k] = U[i][k] + alpha * (2 * error_i_j * V[k][j] - beta * U[i][k])
                        V[k][j] = V[k][j] + alpha * (2 * error_i_j * U[i][k] - beta * V[k][j])
        # 定义损失误差
        loss = 0.0
        for i in xrange(m):
            for j in xrange(n):
                if R[i][j] > 0:
                    # 套用损失函数的公式 (包括下面的循环，其实这里就是把损失函数公式分开写了)
                    loss = loss + pow(R[i][j] - np.dot(U[i, :], V[:, j]), 2)
                    for k in xrange(K):
                        loss = loss + (beta / 2) * (pow(U[i][k], 2) + pow(V[k][j], 2))

        if loss < 0.01:
            print 'when loss = ' + str(loss) + ',epoch break. and step = ' + str(step)
            break
        if step % 1000 == 0:
            print 'step = ' + str(step) + ',and loss = ' + str(loss)
    return U, V


'''
梯度下降法
'''


def lmf(data, K):
    m = len(data)  # 用户数目
    n = len(data[0])  # 物品数目
    # 随机生成一个m*K的矩阵(user)
    u = np.random.rand(m, K)
    # 随机生成一个K*n的矩阵(item)
    v = np.random.rand(n, K)

    # 学习率(梯度)
    alpha = 0.01
    # 惩罚因子
    beta = 0.01
    # 最大迭代次数
    maxEpoches = 1000

    # 开始迭代
    for step in xrange(maxEpoches):
        for i in xrange(m):
            for j in xrange(n):
                if math.fabs(data[i][j]) > 1e-4:  # 只预测非0元素
                    # 当前误差
                    error = data[i][j] - np.dot(u[i], v[j])
                    for k in xrange(K):
                        gu = error * v[j][k] - beta * u[i][k]
                        gv = error * u[i][k] - beta * v[j][k]
                        u[i][k] += alpha * gu
                        v[j][k] += alpha * gv
    return u, v


import scipy.sparse as sparse

if __name__ == "__main__":
    # 原始评分矩阵
    R = load_data("./data/als_test.txt")
    # U, V = gradient_descent(R,K)
    # result = np.dot(U,V)
    # print result

    #
    R = np.mat(R)
    A = np.dot(R,R.T)

    print A


    print A.I

    print np.linalg.inv(A)

    # print np.dot(R,R.I)

    # K = 2
    # U, V = als(R, K)
    # result = np.dot(U, V.T)

    # row = np.array([0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4])
    # col = np.array([0, 1, 3, 0, 3, 0, 1, 3, 0, 3, 1, 2, 3])
    # data = np.array([5, 3, 1, 4, 1, 1, 1, 5, 1, 4, 1, 5, 4])
    # Cui = sparse.coo_matrix((data, (row, col)),shape=(5,4), dtype=np.float64)
    # print(Cui)
    # U, V = implicit_mf.alternating_least_squares(Cui, factors=K)
    # result = np.dot(U, V.T)
    # print result

    # n = len(result)
    # x = range(n)
    # plot(x, result, color='r', linewidth=3)
    # plt.title('Convergence curve')
    # plt.xlabel('generation')
    # plt.ylabel('loss')
    # show()
    pass
