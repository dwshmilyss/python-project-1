#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: plot_demo.py
@time: 2017/7/7 12:01
"""

import numpy as np
import matplotlib.pyplot as plt
def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == "__main__":


    # Make some fake data.
    a = b = np.arange(0, 3, .02)
    c = np.exp(a)
    d = c[::-1]
    print c
    print d

    # Create plots with pre-defined labels.
    fig, ax = plt.subplots()
    ax.plot(a, c, 'k--', label='Model length')
    ax.plot(a, d, 'k:', label='Data length')
    ax.plot(a, c + d, 'k', label='Total message length')

    '''
    right
	center left
	upper right
	lower right
	best
	center
	lower left
	center right
	upper left
	upper center
	lower center
    '''
    legend = ax.legend(loc='upper left', shadow=True, fontsize='x-large')

    # Put a nicer background color on the legend.
    legend.get_frame().set_facecolor('#00FFCC')

    plt.scatter
    plt.show()
    pass