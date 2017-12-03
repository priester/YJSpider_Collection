# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook
class CsHousePipeline(object):
	def __init__(self):
		self.wb = Workbook()
		self.ws = self.wb.active
		self.ws.append(['楼盘名字','楼盘区域','楼盘地址','楼盘类型','楼盘均价'])

	def process_item(self,item,spider):
		line = [item['loupan_title'],item['loupan_region'],item['loupan_detailAddress'],item['loupan_type'],item['average_price']]
		self.ws.append(line)
		self.wb.save('../cs_loupan.xlsx')
		return item

