# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CsHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    loupan_title = scrapy.Field()
    average_price = scrapy.Field()
    loupan_region = scrapy.Field()
    loupan_detailAddress = scrapy.Field()
    loupan_type = scrapy.Field()

