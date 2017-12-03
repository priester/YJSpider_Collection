# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CsErshoufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 房子的位置
    house_locaiton = scrapy.Field()
    # 房子的类型，比如3室2厅
    house_type = scrapy.Field()
    # 房子的面积
    house_area = scrapy.Field()
    # 房子的装修情况
    house_decoration = scrapy.Field()
    # 房子的总价
    house_totalPrice = scrapy.Field()
    # 房子的单价
    house_unitPrice = scrapy.Field()
    
