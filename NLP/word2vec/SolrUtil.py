#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: SolrUtil.py
@time: 2017/6/19 16:16
"""

import urllib2
from xml.sax.saxutils import escape, quoteattr


class MySolrPy():
    def __init__(self, solrurl):
        self.solrurl = solrurl + '/update/'
        print self.solrurl
        self.docs = []
        self.size = 0
        # 添加新的文档

    def add(self, doc):
        self.docs.append(doc)
        self.size += 1
        if self.size >= 30000:
            print self.size
            self.commit()
            self.docs = []
            self.size = 0
            # 提交数据

    def _commit(self, data):
        requestAdd = urllib2.Request(
            url=self.solrurl,
            headers={'Content-type': 'text/xml; charset=utf-8'},
        )
        requestCommit = urllib2.Request(
            url=self.solrurl,
            headers={'Content-type': 'text/xml'},
        )

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        responseAdd = opener.open(requestAdd, data)

        responseCommit = opener.open(requestCommit, '<commit/>')

        # 根据指定的id删除索引

    def delDoc(self, id):
        lst = [u'<delete><id>']
        lst.append('%s' % (escape(unicode(id))))
        lst.append(u'</id></delete>')
        data = ''.join(lst)
        self._commit(data)
        # 删除所有数据

    def delAll(self):
        delCommond = '<delete><query>*:*</query></delete>'
        self._commit(delCommond)
        # 用于新增索引时提交数据

    def commit(self):
        lst = [u'<add>']

        for doc in self.docs:
            newdoc = self.packagingDoc(lst, doc)
        lst.append(u'</add>')
        data = ''.join(lst).encode('utf-8')
        self._commit(data)
        # 包装数据

    def packagingDoc(self, lst, doc):

        lst.append(u'<doc>')
        for k, v in doc.items():
            lst.append('<field name=%s>%s</field>' % (
                (quoteattr(k),
                 escape(unicode(v)))))
        lst.append('</doc>')