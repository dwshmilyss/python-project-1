#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: Lieb
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: CSDNBlogSpider.py
@time: 2017/4/1 19:35
"""

from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from CSDNBlog.items import CsdnblogItem


class CSDNBlogSpider(Spider):
    """爬虫CSDNBlogSpider"""

    name = "CSDNBlog"

    # 减慢爬取速度 为1s
    download_delay = 1
    allowed_domains = ["blog.csdn.net"]
    start_urls = [

        # 第一篇文章地址
        "http://blog.csdn.net/u012150179/article/details/11749017"
    ]

    def parse(self, response):
        sel = Selector(response)

        # items = []
        # 获得文章url和标题
        item = CsdnblogItem()

        article_url = str(response.url)
        article_name = sel.xpath('//div[@id="article_details"]/div/h1/span/a/text()').extract()

        item['article_name'] = [n.encode('utf-8') for n in article_name]
        item['article_url'] = article_url.encode('utf-8')

        yield item

        # 获得下一篇文章的url
        urls = sel.xpath('//li[@class="next_article"]/a/@href').extract()
        for url in urls:
            print url
            url = "http://blog.csdn.net" + url
            print url
            yield Request(url, callback=self.parse)