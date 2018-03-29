# -*- coding: utf-8 -*-
import scrapy


class HsYoujiSpider(scrapy.Spider):
    name = 'hs_youji'
    allowed_domains = ['http://www.mafengwo.cn/yj/11886/']
    start_urls = ['http://http://www.mafengwo.cn/yj/11886//']

    def parse(self, response):
        pass
