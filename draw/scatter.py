#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: scatter.py
@time: 2017/6/28 15:51
"""
import numpy as np
import operator
from matplotlib import pyplot as plt


def createDateSet():
    group = np.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

#带标签
def demo1():
    group, labels = createDateSet()
    f = plt.figure(figsize=(8, 4))
    # ax = f.add_subplot(111)
    # ax.set_title("A blob with 3 centers")
    plt.title("A blob with 3 centers")
    colors = np.array(['r', 'g'])

    #加入labels
    for i in xrange(0,group.__len__()):
        plt.annotate(
            '%s' % labels[i],
            xy=(group[i][0], group[i][1]),
            xytext=(-10, 0),
            textcoords='offset points',
            ha='center',
            # (u'top', u'bottom', u'center', u'baseline')
            va='center')

    plt.scatter(group[:, 0], group[:, 1],  marker = 'o', color = colors, label='aa', s = 50)
    plt.show()


def demo2():
    x_coords = [0.13, 0.22, 0.39, 0.59, 0.68, 0.74, 0.93]
    y_coords = [0.75, 0.34, 0.44, 0.52, 0.80, 0.25, 0.55]

    fig = plt.figure(figsize=(8, 5))
    plt.scatter(x_coords, y_coords, marker='s', s=50)

    for x, y in zip(x_coords, y_coords):
        plt.annotate(
            '(%s %s)' % (x,y),
            xy=(x, y),
            xytext=(0, -10),
            textcoords='offset points',
            ha='center',
            # (u'top', u'bottom', u'center', u'baseline')
            va='top')

    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.show()

def demo3():
    mu_vec1 = np.array([0, 0])
    cov_mat1 = np.array([[2, 0], [0, 2]])

    x1_samples = np.random.multivariate_normal(mu_vec1, cov_mat1, 100)
    x2_samples = np.random.multivariate_normal(mu_vec1 + 0.2, cov_mat1 + 0.2, 100)
    x3_samples = np.random.multivariate_normal(mu_vec1 + 0.4, cov_mat1 + 0.4, 100)

    # x1_samples.shape -> (100, 2), 100 rows, 2 columns

    plt.figure(figsize=(8, 6))

    plt.scatter(x1_samples[:, 0], x1_samples[:, 1], marker='x',
                color='blue', alpha=0.7, label='x1 samples')
    plt.scatter(x2_samples[:, 0], x1_samples[:, 1], marker='o',
                color='green', alpha=0.7, label='x2 samples')
    plt.scatter(x3_samples[:, 0], x1_samples[:, 1], marker='^',
                color='red', alpha=0.7, label='x3 samples')
    plt.title('Basic scatter plot')
    plt.ylabel('variable X')
    plt.xlabel('Variable Y')
    plt.legend(loc='upper right')

    plt.show()

# 用曲线把样本分成两类
def demo4():
    def decision_boundary(x_1):
        """ Calculates the x_2 value for plotting the decision boundary."""
        return 4 - np.sqrt(-x_1 ** 2 + 4 * x_1 + 6 + np.log(16))

    # Generating a Gaussion dataset:
    # creating random vectors from the multivariate normal distribution
    # given mean and covariance
    mu_vec1 = np.array([0, 0])
    cov_mat1 = np.array([[2, 0], [0, 2]])
    x1_samples = np.random.multivariate_normal(mu_vec1, cov_mat1, 100)
    mu_vec1 = mu_vec1.reshape(1, 2).T  # to 1-col vector

    mu_vec2 = np.array([1, 2])
    cov_mat2 = np.array([[1, 0], [0, 1]])
    x2_samples = np.random.multivariate_normal(mu_vec2, cov_mat2, 100)
    mu_vec2 = mu_vec2.reshape(1, 2).T  # to 1-col vector

    # Main scatter plot and plot annotation
    f, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(x1_samples[:, 0], x1_samples[:, 1], marker='o', color='green', s=40, alpha=0.5)
    ax.scatter(x2_samples[:, 0], x2_samples[:, 1], marker='^', color='blue', s=40, alpha=0.5)
    plt.legend(['Class1 (w1)', 'Class2 (w2)'], loc='upper right')
    plt.title('Densities of 2 classes with 25 bivariate random patterns each')
    plt.ylabel('x2')
    plt.xlabel('x1')
    ftext = 'p(x|w1) ~ N(mu1=(0,0)^t, cov1=I)np(x|w2) ~ N(mu2=(1,1)^t, cov2=I)'
    plt.figtext(.15, .8, ftext, fontsize=11, ha='left')

    # Adding decision boundary to plot
    x_1 = np.arange(-5, 5, 0.1)
    bound = decision_boundary(x_1)
    plt.plot(x_1, bound, 'r--', lw=3)

    x_vec = np.linspace(*ax.get_xlim())
    x_1 = np.arange(0, 100, 0.05)

    plt.show()

class Main():
    def __init__(self):
        pass


if __name__ == "__main__":
    demo4()
    pass