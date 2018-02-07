#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: implicit_mf.py
@time: 2017/9/26 16:39
"""
import sys

default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.sparse as sparse
import pickle
import csv
import implicit
import itertools
import copy
plt.style.use('ggplot')


class Main():
    def __init__(self):
        pass


'''
按条件过滤数据
uid_min 过滤出用户查看次数 >=uid_min 的数据
mid_min 过滤出物品被查看次数 >=mid_min 的数据
'''


def threshold_likes(df, uid_min, mid_min):
    # 获取有多少用户
    n_users = df.uid.unique().shape[0]
    # 获取有多少item
    n_items = df.mid.unique().shape[0]
    # 稀疏程度 值越小越稀疏
    sparsity = float(df.shape[0]) / float(n_users * n_items) * 100
    print('Starting likes info')
    print('Number of users: {}'.format(n_users))
    print('Number of models: {}'.format(n_items))
    print('Sparsity: {:4.3f}%'.format(sparsity))

    done = False
    while not done:
        starting_shape = df.shape[0]
        # 按uid分组 得到的数据就是每个用户查看了多少次 其实按我的理解这里应该是uid_counts
        uid_counts = df.groupby('uid').mid.count()
        # 过滤掉用户查看次数小于mid_min的数据 ~：取非
        df = df[~df.uid.isin(uid_counts[uid_counts < uid_min].index.tolist())]
        # 按mid分组 得到的数据就是每个item被查看了多少次 其实按我的理解这里应该是mid_counts
        mid_counts = df.groupby('mid').uid.count()
        # 过滤掉item被查看次数小于mid_min的数据
        df = df[~df.mid.isin(mid_counts[mid_counts < mid_min].index.tolist())]
        # 循环直到再也不能过滤数据为止
        ending_shape = df.shape[0]
        if starting_shape == ending_shape:
            done = True
    # 断言 所以这里的
    assert (df.groupby('uid').mid.count().min() >= uid_min)
    assert (df.groupby('mid').uid.count().min() >= mid_min)

    n_users = df.uid.unique().shape[0]
    n_items = df.mid.unique().shape[0]
    sparsity = float(df.shape[0]) / float(n_users * n_items) * 100
    print('Ending likes info')
    print('Number of users: {}'.format(n_users))
    print('Number of models: {}'.format(n_items))
    print('Sparsity: {:4.3f}%'.format(sparsity))
    return df


'''
切分训练集和测试集
'''


def train_test_split(ratings, split_count, fraction=None):
    """
    Split recommendation data into train and test sets

    Params
    ------
    ratings : scipy.sparse matrix
        Interactions between users and items.
    split_count : int
        Number of user-item-interactions per user to move
        from training to test set.
    fractions : float
        Fraction of users to split off some of their
        interactions into test set. If None, then all 
        users are considered.
    """
    # Note: likely not the fastest way to do things below.
    train = ratings.copy().tocoo()
    test = sparse.lil_matrix(train.shape)

    if fraction:
        try:
            # 这里就是从8000多个用户中随机挑选出3054个用户 作为测试集
            user_index = np.random.choice(
                # 获取查看次数 >= split_count * 2 的用户ID的index，这里有8000多个用户
                np.where(np.bincount(train.row) >= split_count * 2)[0],
                replace=False,
                # 总人数的0.2 = 3054
                size=np.int32(np.floor(fraction * train.shape[0]))
            ).tolist()
        except:
            print(('Not enough users with > {} '
                   'interactions for fraction of {}') \
                  .format(2 * k, fraction))
            raise
    else:
        user_index = range(train.shape[0])

    train = train.tolil()

    for user in user_index:
        test_ratings = np.random.choice(ratings.getrow(user).indices,
                                        size=split_count,
                                        replace=False)
        train[user, test_ratings] = 0.
        # These are just 1.0 right now
        test[user, test_ratings] = ratings[user, test_ratings]

    # Test and training are truly disjoint
    assert (train.multiply(test).nnz == 0)
    return train.tocsr(), test.tocsr(), user_index

""" Implicit Alternating Least Squares """
import numpy as np
import time
import os
import logging

log = logging.getLogger("implicit")

'''
交替最小二乘法求解矩阵分解(别人重写的)
'''
class ALS(object):

    def __init__(self,
                 num_factors=40,
                 regularization=0.01,
                 alpha=1.0,
                 iterations=15,
                 use_native=True,
                 num_threads=0,
                 dtype=np.float64):
        """
        Class version of alternating least squares implicit matrix factorization

        Args:
            num_factors (int): Number of factors to extract
            regularization (double): Regularization parameter to use
            iterations (int): Number of alternating least squares iterations to
            run
            use_native (bool): Whether or not to use Cython solver
            num_threads (int): Number of threads to run least squares iterations.
            0 means to use all CPU cores.
            dtype (np dtype): Datatype for numpy arrays
        """
        self.num_factors = num_factors
        self.regularization = regularization
        self.alpha = alpha
        self.iterations = iterations
        self.use_native = use_native
        self.num_threads = num_threads
        self.dtype = dtype

    def fit(self, Cui):
        """
        Fit an alternating least squares model on Cui data

        Args:
            Cui (sparse matrix, shape=(num_users, num_items)): Matrix of
            user-item "interactions"
        """

        _check_open_blas()

        users, items = Cui.shape

        self.user_vectors = np.random.normal(size=(users, self.num_factors))\
                                     .astype(self.dtype)

        self.item_vectors = np.random.normal(size=(items, self.num_factors))\
                                     .astype(self.dtype)

        '''
        use_native 是否是隐式矩阵分解 true:没有评分
        '''
        self.solver = implicit.als.least_squares if self.use_native else least_squares

        self.fit_partial(Cui)

    def fit_partial(self, Cui):
        """Continue fitting model"""

        # Scaling
        Cui = Cui.copy()
        Cui.data *= self.alpha
        Cui, Ciu = Cui.tocsr(), Cui.T.tocsr()

        for iteration in range(self.iterations):
            s = time.time()
            self.solver(Cui,
                        self.user_vectors,
                        self.item_vectors,
                        self.regularization,
                        self.num_threads)
            self.solver(Ciu,
                        self.item_vectors,
                        self.user_vectors,
                        self.regularization,
                        self.num_threads)
            log.debug("finished iteration %i in %s", iteration, time.time() - s)

    def predict(self, user, item):
        """Predict for single user and item"""
        return self.user_vectors[user, :].dot(self.item_vectors[item, :].T)

    def predict_for_customers(self,):
        """Recommend products for all customers"""
        return self.user_vectors.dot(self.item_vectors.T)

    def predict_for_items(self, norm=True):
        """Recommend products for all products"""
        pred = self.item_vectors.dot(self.item_vectors.T)
        if norm:
            norms = np.array([np.sqrt(np.diagonal(pred))])
            pred = pred / norms / norms.T
        return pred

def alternating_least_squares(Cui, factors, regularization=0.01,
                              iterations=15, use_native=True, num_threads=0,
                              dtype=np.float64):
    """ factorizes the matrix Cui using an implicit alternating least squares
    algorithm

    Args:
        Cui (csr_matrix): Confidence Matrix
        factors (int): Number of factors to extract
        regularization (double): Regularization parameter to use
        iterations (int): Number of alternating least squares iterations to
        run
        num_threads (int): Number of threads to run least squares iterations.
        0 means to use all CPU cores.

    Returns:
        tuple: A tuple of (row, col) factors
    """
    _check_open_blas()

    users, items = Cui.shape

    X = np.random.rand(users, factors).astype(dtype) * 0.01
    Y = np.random.rand(items, factors).astype(dtype) * 0.01

    Cui, Ciu = Cui.tocsr(), Cui.T.tocsr()

    solver = implicit.als.least_squares if use_native else least_squares

    for iteration in range(iterations):
        s = time.time()
        solver(Cui, X, Y, regularization, num_threads)
        solver(Ciu, Y, X, regularization, num_threads)
        log.debug("finished iteration %i in %s", iteration, time.time() - s)

    return X, Y


def least_squares(Cui, X, Y, regularization, num_threads):
    """ For each user in Cui, calculate factors Xu for them
    using least squares on Y.

    Note: this is at least 10 times slower than the cython version included
    here.
    """
    users, factors = X.shape
    YtY = Y.T.dot(Y)

    for u in range(users):
        # accumulate YtCuY + regularization*I in A
        A = YtY + regularization * np.eye(factors)

        # accumulate YtCuPu in b
        b = np.zeros(factors)

        for i, confidence in nonzeros(Cui, u):
            factor = Y[i]
            A += (confidence - 1) * np.outer(factor, factor)
            b += confidence * factor

        # Xu = (YtCuY + regularization * I)^-1 (YtCuPu)
        X[u] = np.linalg.solve(A, b)


def nonzeros(m, row):
    """ returns the non zeroes of a row in csr_matrix """
    for index in range(m.indptr[row], m.indptr[row+1]):
        yield m.indices[index], m.data[index]


def _check_open_blas():
    """ checks to see if using OpenBlas. If so, warn if the number of threads isn't set to 1
    (causes perf issues) """
    if np.__config__.get_info('openblas_info') and os.environ.get('OPENBLAS_NUM_THREADS') != '1':
        log.warn("OpenBLAS detected. Its highly recommend to set the environment variable "
                 "'export OPENBLAS_NUM_THREADS=1' to disable its internal multithreading")

'''
 ALS end.....
'''

from sklearn.metrics import mean_squared_error


def calculate_mse(model, ratings, user_index=None):
    preds = model.predict_for_customers()
    if user_index:
        return mean_squared_error(ratings[user_index, :].toarray().ravel(),
                                  preds[user_index, :].ravel())

    return mean_squared_error(ratings.toarray().ravel(),
                              preds.ravel())


def precision_at_k(model, ratings, k=5, user_index=None):
    if not user_index:
        user_index = range(ratings.shape[0])
    ratings = ratings.tocsr()
    precisions = []
    # Note: line below may become infeasible for large datasets.
    predictions = model.predict_for_customers()
    for user in user_index:
        # In case of large dataset, compute predictions row-by-row like below
        # predictions = np.array([model.predict(row, i) for i in xrange(ratings.shape[1])])
        top_k = np.argsort(-predictions[user, :])[:k]
        labels = ratings.getrow(user).indices
        precision = float(len(set(top_k) & set(labels))) / float(k)
        precisions.append(precision)
    return np.mean(precisions)


def print_log(row, header=False, spacing=12):
    top = ''
    middle = ''
    bottom = ''
    for r in row:
        top += '+{}'.format('-' * spacing)
        if isinstance(r, str):
            middle += '| {0:^{1}} '.format(r, spacing - 2)
        elif isinstance(r, int):
            middle += '| {0:^{1}} '.format(r, spacing - 2)
        elif isinstance(r, float):
            middle += '| {0:^{1}.5f} '.format(r, spacing - 2)
        bottom += '+{}'.format('=' * spacing)
    top += '+'
    middle += '|'
    bottom += '+'
    if header:
        print(top)
        print(middle)
        print(bottom)
    else:
        print(middle)
        print(top)


def learning_curve(model, train, test, epochs, k=5, user_index=None):
    if not user_index:
        user_index = range(train.shape[0])
    prev_epoch = 0
    train_precision = []
    train_mse = []
    test_precision = []
    test_mse = []

    headers = ['epochs', 'p@k train', 'p@k test',
               'mse train', 'mse test']
    print_log(headers, header=True)

    for epoch in epochs:
        model.iterations = epoch - prev_epoch
        if not hasattr(model, 'user_vectors'):
            model.fit(train)
        else:
            model.fit_partial(train)
        train_mse.append(calculate_mse(model, train, user_index))
        train_precision.append(precision_at_k(model, train, k, user_index))
        test_mse.append(calculate_mse(model, test, user_index))
        test_precision.append(precision_at_k(model, test, k, user_index))
        row = [epoch, train_precision[-1], test_precision[-1],
               train_mse[-1], test_mse[-1]]
        print_log(row)
        prev_epoch = epoch
    return model, train_precision, train_mse, test_precision, test_mse


def grid_search_learning_curve(base_model, train, test, param_grid,
                               user_index=None, patk=5, epochs=range(2, 40, 2)):
    """
    "Inspired" (stolen) from sklearn gridsearch
    https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/model_selection/_search.py
    """
    curves = []
    keys, values = zip(*param_grid.items())
    for v in itertools.product(*values):
        params = dict(zip(keys, v))
        this_model = copy.deepcopy(base_model)
        print_line = []
        for k, v in params.items():
            setattr(this_model, k, v)
            print_line.append((k, v))

        print(' | '.join('{}: {}'.format(k, v) for (k, v) in print_line))
        _, train_patk, train_mse, test_patk, test_mse = learning_curve(this_model, train, test,
                                                                       epochs, k=patk, user_index=user_index)
        curves.append({'params': params,
                       'patk': {'train': train_patk, 'test': test_patk},
                       'mse': {'train': train_mse, 'test': test_mse}})
    return curves


if __name__ == "__main__":
    # read_csv()中的路径./指的是项目的根目录(即工作路径)
    df = pd.read_csv('../../data/model_likes_anon.psv',
                     sep='|', quoting=csv.QUOTE_MINIMAL,
                     quotechar='\\')
    df.head()
    # 获取表中重复记录的条数
    print('Duplicated rows: ' + str(df.duplicated().sum()))
    print('That\'s weird - let\'s just drop them')
    # 删除重复的记录
    df.drop_duplicates(inplace=True)
    df = df[['uid', 'mid']]
    df.head()
    print df.shape[0]
    df_lim = threshold_likes(df, 5, 5)
    '''
    创建idx -> uid   idx -> item的映射
    idx由enumerate生产，从0开始 step为1  依次递增
    '''
    mid_to_idx = {}
    idx_to_mid = {}
    for (idx, mid) in enumerate(df_lim.mid.unique().tolist()):
        mid_to_idx[mid] = idx
        idx_to_mid[idx] = mid

    uid_to_idx = {}
    idx_to_uid = {}
    for (idx, uid) in enumerate(df_lim.uid.unique().tolist()):
        uid_to_idx[uid] = idx
        idx_to_uid[idx] = uid

    def map_ids(row, mapper):
        return mapper[row]

    # 获取uid对应的idx，返回成矩阵的形式，也就是numpy.ndarray
    I = df_lim.uid.apply(map_ids, args=[uid_to_idx]).as_matrix()
    # 获取item对应的idx，返回
    J = df_lim.mid.apply(map_ids, args=[mid_to_idx]).as_matrix()
    # 根据uid的维度构建一个单位矩阵(在这里就是一个一维的向量)
    V = np.ones(I.shape[0])
    # 按坐标存储稀疏矩阵 I,J为坐标  V是值
    likes = sparse.coo_matrix((V, (I, J)), dtype=np.float64)
    # 按行压缩 比如同一个坐标出现了3次1 那么这个位置就是3
    likes = likes.tocsr()
    print likes.shape
    '''
        按0.2的比例切分成训练集和测试集
    '''
    train, test, user_index = train_test_split(likes, 2, fraction=0.2)

    param_grid = {'num_factors': [10, 20, 40, 80, 120],
                  'regularization': [0.0, 1e-5, 1e-3, 1e-1, 1e1, 1e2],
                  'alpha': [1, 10, 50, 100, 500, 1000]}

    base_model = ALS()

    curves = grid_search_learning_curve(base_model, train, test,
                                        param_grid,
                                        user_index=user_index,
                                        patk=5)

    pass