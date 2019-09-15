# -*- coding: utf-8 -*-
import scrapy


class SpiderCsdnSpider(scrapy.Spider):
    name = 'spider_csdn'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net/']

    def parse(self, response):
        print response.url  # 打印当前爬取的链接
        print response.body  # 打印当前爬取网页的源代码
        pass
