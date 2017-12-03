# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook
class CsErshoufangPipeline(object):
    def process_item(self, item, spider):
    	line = [item['house_locaiton'],item['house_type'],item['house_area'],item['house_decoration'],item['house_totalPrice'],item['house_unitPrice']]
    	self.ws.append(line)
    	self.wb.save('./cs_ershoufang.xlsx')
        return item

    def __init__(self):
    	self.wb = Workbook()
    	self.ws = self.wb.active
    	self.ws.append(['房子位置','房子类型','房子面积','房子装修','房子总价','房子单价'])
