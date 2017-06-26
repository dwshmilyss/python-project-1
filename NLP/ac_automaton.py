#encoding:utf-8
#!/usr/bin/python

'''
AC自动机实现大数据量的敏感词过滤
'''

import time
import ahocorasick
import codecs
import esm
from acora import AcoraBuilder

dictFile = "data/dict.txt"
testFile = "data/content1.txt"

class Ahocorasick(object):
    def __init__(self,dic):
        ahocorasick
        self.__tree = ahocorasick.Automaton()
        # 向trie树中添加单词
        with open(dic, 'r') as fp:
            for line in fp:
                bkw = line.strip()
                self.__tree.add_word(bkw, (1, bkw))
        fp.close()
        # 将trie树转化为Aho-Corasick自动机
        self.__tree.make_automaton()

    def findall(self,content):
        hitList = []
        for start, end in self.__tree.find_all(content):
            hitList.append(content[start:end])
        return hitList

class Acora(object):

    def __init__(self,dic):
        self.__builder = AcoraBuilder()
        fp = open(dic)
        for line in fp:
            word = line.strip().decode("utf-8")
            self.__builder.add(word)
        fp.close()
        self.__tree = self.__builder.build()

    def findall(self,content):
        print content
        hitList = []
        #pos为startIndex
        for hitWord, pos in self.__tree.finditer(content):
            print (pos,hitWord)
            hitList.append(hitWord)
        return hitList

class Esmre(object):

    def __init__(self,dic):
        self.__index = esm.Index()
        fp = open(dic)
        for line in fp:
            self.__index.enter(line.rstrip("n"))
        fp.close()
        self.__index.fix()

    def findall(self,content):
        hitList = []
        for pos, hitWord in self.__index.query(content):
            hitList.append(hitWord)
        return hitList

if __name__ == "__main__":
    pass
    fp = open(testFile)
    content = fp.read()
    fp.close()
    #
    # t0 = time.time()
    # ahocorasick_obj = Ahocorasick(dictFile)
    # t1 = time.time()
    # acora_obj = Acora(dictFile)
    # t2 = time.time()
    # esmre_obj = Esmre(dictFile)
    # t3 = time.time()
    #
    # # ahocorasick_obj.findall(content)
    # t4 = time.time()
    # acora_obj.findall(content.decode("utf-8"))
    # for word in acora_obj.findall(content.decode("utf-8")):
    #     print word
    # t5 = time.time()
    # esmre_obj.findall(content)
    # t6 = time.time()
    #
    # Ahocorasick_init = t1 - t0
    # Acora_init = t2 - t1
    # Esmre_init = t3 - t2
    # Ahocorasick_process = t4 - t3
    # Acora_process = t5 - t4
    # Esmre_process = t6 - t5
    # print "Ahocorasick init: %f" % Ahocorasick_init
    # print "Acora init: %f" % Aco.ra_init
    # print "Esm_init: %f" % Esmre_init
    # print "Ahocorasick process: %s" % Ahocorasick_process
    # print "Acora process: %s" % Acora_process
    # print "Esm_process: %f" % Esmre_process

    t1 = time.time()
    A = ahocorasick.Automaton()
    # 向trie树中添加单词
    for idx, key in enumerate('he her hers she'.split()):
        A.add_word(key, (idx, key))
    # 将trie树转化为Aho-Corasick自动机
    A.make_automaton()

    content = 'mine is he and you'
    # for start, end in A.find_all(content):
    #     print content[start:end]

    def callback(endIndex,value):
        print (endIndex,value)

    A.find_all(content,callback)
    # for end_index, (idx,original_value) in A.iter(content):
    #     start_index = end_index - len(original_value) + 1
    #     print((start_index, end_index, (idx, original_value)))
    # g1 = open("result_dangdang.txt", 'a+')
    # for line in open("dangdang.txt"):
    #     for k, (i, t) in A.iter(line.strip()):
    #         print line.strip() + t
    #         g1.write(line.strip() + ":" + t + "\n")
    # g1.close()
    t2 = time.time()
    print "cost time is ", t2 - t1