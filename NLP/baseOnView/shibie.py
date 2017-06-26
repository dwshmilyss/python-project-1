#! -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
from tqdm import tqdm
import re
import time
import os

print u'read data ...'
train_data = pd.read_csv('Train.csv', index_col='SentenceId', delimiter='\t', encoding='utf-8')
test_data = pd.read_csv('Test.csv', index_col='SentenceId', delimiter='\t', encoding='utf-8')
train_label = pd.read_csv('Label.csv', index_col='SentenceId', delimiter='\t', encoding='utf-8')
addition_data = pd.read_csv('addition_data.csv', header=None, encoding='utf-8')[0]
train_data.dropna(inplace=True) # drop some empty sentences
neg_data = pd.read_excel('neg.xls', header=None)[0]
pos_data = pd.read_excel('pos.xls', header=None)[0]

script_name = 'shibie.py'
now = int(time.time())
os.system('mkdir %s'%now)
os.system('cp %s %s'%(script_name, now))
os.system('cp addition_data.csv %s'%now)

# soma parameters
min_count = 5
maxlen = 100
word_size = 64

print u'making mapping dictionary ...'
word2id = ''.join(train_data['Content']) + ''.join(test_data['Content']) + ''.join(addition_data)
word2id = pd.Series(list(word2id)).value_counts()
word2id = word2id[word2id >= min_count]
word2id[:] = range(1, len(word2id)+1)
print u'keep %s words.'%len(word2id)

def doc2id(s):
    return list(word2id[list(s)].fillna(len(word2id)+1).astype(np.int32))

print u'translating texts into id sequences ...'
train_data['doc2id'] = map(lambda i: doc2id(train_data.loc[i, 'Content']), tqdm(iter(train_data.index)))
test_data['doc2id'] = map(lambda i: doc2id(test_data.loc[i, 'Content']), tqdm(iter(test_data.index)))
addition_data[:] = map(lambda i: doc2id(addition_data[i]), tqdm(iter(addition_data.index)))
pos_data[:] = map(lambda i: doc2id(pos_data[i]), tqdm(iter(pos_data.index)))
neg_data[:] = map(lambda i: doc2id(neg_data[i]), tqdm(iter(neg_data.index)))

# make n-grams for train language model
n = 8
def gen_ngrams(s):
    s = [0]*(n-1) + s + [0]*(n-1)
    return zip(*[s[i:] for i in range(n)])

print u'generating ngrams ...'
from itertools import chain
ngrams = pd.concat([train_data['doc2id'].apply(gen_ngrams),
                    test_data['doc2id'].apply(gen_ngrams),
                    addition_data.apply(gen_ngrams),
                    pos_data.apply(gen_ngrams),
                    neg_data.apply(gen_ngrams)])
ngrams = np.array(list(chain(*ngrams)))

def findall(sub_string, string):
    start = 0
    idxs = []
    while True:
        idx = string[start:].find(sub_string)
        if idx == -1:
            return idxs
        else:
            idxs.append(start + idx)
            start += idx + len(sub_string)

tags = {'pos':1, 'neu':2, 'neg':3}

def label2tag(i):
    s = train_data.loc[i]['Content']
    r = np.array([0]*len(s))
    try:
        l = train_label.loc[[i]].as_matrix()
    except:
        return r
    for i in l:
        for j in findall(i[0], s):
            r[j:j+len(i[0])] = tags[i[1]]
    return r

print u'translating target into tags ...'
train_data['label'] = map(label2tag, tqdm(iter(train_data.index)))
print u'keep %s train sample.'%len(train_data)

from keras.layers import Input, Embedding, GRU, Dense, TimeDistributed, Bidirectional
from keras.models import Model
from keras.utils import np_utils

RNN = GRU # which type of RNN we used, try LSTM or GRU

# in order to gain good word embedding, we use GRU to train a n-grams language model
# it costs more time, but it produces better word embedding.
print u'training language model ...'
lm_input = Input(shape=(n-1,), dtype='int32')
lm_embedded = Embedding(len(word2id)+2,
                         word_size,
                         input_length=n-1,
                         mask_zero=True)(lm_input)
lm_rnn = RNN(64)(lm_embedded)
lm_output = Dense(len(word2id)+2, activation='softmax')(lm_rnn)
language_model = Model(input=lm_input, output=lm_output)
language_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

def lm_generator(ngrams, batch_size):
    while True:
        np.random.shuffle(ngrams)
        for p in np.split(ngrams, range(batch_size, len(ngrams), batch_size)):
            yield p[:, :-1], np_utils.to_categorical(p[:, -1], len(word2id)+2)

nb_epoch = 8 # accuracy changes slightly after 5 epoch
batch_size = 4096
lm_history = language_model.fit_generator(lm_generator(ngrams, batch_size), nb_epoch=nb_epoch, samples_per_epoch=len(ngrams))
language_model.save_weights('%s/language_model_weights.model'%now)
structure = open('%s/language_model_structure.model'%now, 'w')
structure.write(language_model.to_json())
structure.close()

# here we use 2 layers of bidirectional GRU to make a sequence tagging model
print u'training ner model ...'
ner_input = Input(shape=(maxlen,), dtype='int32')
ner_embedded = Embedding(len(word2id)+2,
                         word_size,
                         input_length=maxlen,
                         mask_zero=True,
                         trainable=False,
                         weights=[language_model.get_weights()[0]])(ner_input)
ner_brnn = Bidirectional(RNN(64, return_sequences=True), merge_mode='sum')(ner_embedded)
ner_brnn = Bidirectional(RNN(32, return_sequences=True), merge_mode='sum')(ner_brnn)
ner_output = TimeDistributed(Dense(5, activation='softmax'))(ner_brnn)
ner_model = Model(input=ner_input, output=ner_output)
ner_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

ner_data = train_data['doc2id'].apply(lambda s: s[:maxlen] + [0]*(maxlen - len(s[:maxlen])))
ner_data = np.array(list(ner_data))
ner_target = train_data['label'].apply(list).apply(lambda s: s[:maxlen] + [0]*(maxlen - len(s[:maxlen])))
ner_target = np.array(list(ner_target))
ner_target = np.array(map(lambda y:np_utils.to_categorical(y,5), ner_target))
sample_weight = (3/(train_data['label'].apply(lambda s:(np.array(s)==2).sum())+3)).as_matrix()

nb_epoch = 300
batch_size = 1024
ner_history_1 = ner_model.fit(ner_data, ner_target, batch_size=batch_size, nb_epoch=nb_epoch, sample_weight=sample_weight)
ner_model.save_weights('%s/ner_model_weights_1.model'%now)
structure = open('%s/ner_model_structure_1.model'%now, 'w')
structure.write(ner_model.to_json())
structure.close()

test_ner_data = test_data['doc2id'].apply(lambda s: s[:maxlen] + [0]*(maxlen - len(s[:maxlen])))
test_ner_data = np.array(list(test_ner_data))

print u'predicting ...'
train_data['predict'] = list(ner_model.predict(ner_data, batch_size=batch_size, verbose=1))
test_data['predict'] = list(ner_model.predict(test_ner_data, batch_size=batch_size, verbose=1))

def viterbi(nodes):
    paths = nodes[0]
    for l in range(1,len(nodes)):
        paths_ = paths.copy()
        paths = {}
        for i in nodes[l].keys():
            nows = {}
            for j in paths_.keys():
                if j[-1]+i in zy.keys():
                    nows[j+i]= paths_[j]+nodes[l][i]+zy[j[-1]+i]
            k = np.argmax(nows.values())
            paths[nows.keys()[k]] = nows.values()[k]
    return paths.keys()[np.argmax(paths.values())]

zy = {'00':1,
      '01':1,
      '02':1,
      '03':1,
      '10':1,
      '11':1,
      '20':1,
      '22':1,
      '30':1,
      '33':1}

zy = {i:np.log(zy[i]) for i in zy.keys()}

from acora import AcoraBuilder
views = pd.read_csv('View.csv', delimiter='\t', encoding='utf-8')['View']
views = AcoraBuilder(*views)
views = views.build()

def predict(i, data):
    y_pred = data.loc[i, 'predict']
    s = data.loc[i, 'Content'][:maxlen]
    nodes = [dict(zip(['0','1','2','3'], k)) for k in np.log(y_pred[:len(s)])]
    tags_pred_1 = viterbi(nodes)
    for j in views.finditer(s):
        for k in range(j[1], j[1]+len(j[0])):
            nodes[k]['1'] += 100
            nodes[k]['2'] += 100
            nodes[k]['3'] += 100
        try:
            nodes[j[1]-1]['0'] += 50
            nodes[k+1]['0'] += 50
        except:
            pass
    tags_pred_2 = viterbi(nodes)
    r = []
    for j in re.finditer('1+|2+|3+', tags_pred_2):
        t = pd.Series(list(tags_pred_1[j.start():j.end()])).value_counts()
        t = t[t.index != '0']
        if len(t) == 0:
            continue
        else:
            if t.index[0] == '1':
                r.append((i, s[j.start():j.end()], 'pos'))
            elif t.index[0] == '2':
                r.append((i, s[j.start():j.end()], 'neu'))
            else:
                r.append((i, s[j.start():j.end()], 'neg'))
    return r

print u'creating the final export ...'
train_data['pred'] = map(lambda i: predict(i, train_data), tqdm(iter(train_data.index)))
test_data['pred'] = map(lambda i: predict(i, test_data), tqdm(iter(test_data.index)))

result_1 = pd.DataFrame(list(chain(*test_data['pred'])), columns=['SentenceId', 'View', 'Opinion'])
result_1 = result_1.drop_duplicates()
result_1.to_csv('%s/result_1.csv'%now, index=None, encoding='utf-8')

# transfer learning
# we use the train result to train ner model again
result_1['SentenceId'] = result_1['SentenceId'].apply(int)
result = result_1.set_index('SentenceId')

def label2tag(i):
    s = test_data.loc[i]['Content']
    r = np.array([0]*len(s))
    try:
        l = result.loc[[i]].as_matrix()
    except:
        return r
    for i in l:
        for j in findall(i[0], s):
            r[j:j+len(i[0])] = tags[i[1]]
    return r

test_data['label'] = map(label2tag, tqdm(iter(test_data.index)))
ner_data = train_data['doc2id'].append(test_data['doc2id']).apply(lambda s: s[:maxlen] + [0]*(maxlen - len(s[:maxlen])))
ner_data = np.array(list(ner_data))
ner_target = train_data['label'].append(test_data['label']).apply(list).apply(lambda s: s[:maxlen] + [0]*(maxlen - len(s[:maxlen])))
ner_target = np.array(list(ner_target))
ner_target = np.array(map(lambda y:np_utils.to_categorical(y, 5), ner_target))

nb_epoch = 100
batch_size = 1024
ner_history_2 = ner_model.fit(ner_data, ner_target, batch_size=batch_size, nb_epoch=nb_epoch)
ner_model.save_weights('%s/ner_model_weights_2.model'%now)
structure = open('%s/ner_model_structure_2.model'%now, 'w')
structure.write(ner_model.to_json())
structure.close()

print u'predicting again ...'
test_data['predict'] = list(ner_model.predict(test_ner_data, batch_size=batch_size, verbose=1))

print u'creating the final export again ...'
test_data['pred'] = map(lambda i: predict(i, test_data), tqdm(iter(test_data.index)))

result_2 = pd.DataFrame(list(chain(*test_data['pred'])), columns=['SentenceId', 'View', 'Opinion'])
result_2 = result_2.drop_duplicates()
result_2.to_csv('%s/result_2.csv'%now, index=None, encoding='utf-8')