# -*- coding: utf-8 -*-
import scrapy
from cs_ershoufang.items import CsErshoufangItem
from bs4 import BeautifulSoup
import re

class ErshoufangSpider(scrapy.Spider):
    name = 'ershoufang'
    allowed_domains = ['cs.lianjia.com']
    start_urls = ['https://cs.lianjia.com/ershoufang/']
    next_page = 2
    toal_page = 58


    def parse(self, response):
    	soup = BeautifulSoup(response.text)

    	print "==============开始解析数据============="
    	uls = soup.find_all('ul',class_='sellListContent')
    	try:
    		for li in uls[0].find_all('li',class_='clear'):
    		# print li.text
	    		item = CsErshoufangItem()
	   
	    		# 房屋信息
	    		infos = li.select('div.info.clear > div.address > div')[0].text.split('|')
	    		# 小区位置
	    		house_locaiton = infos[0]
	    		# 房子的类型，比如3室2厅
	    		house_type = infos[1]
	    		# 房子的面积
	    		house_area = infos[2]
	    		house_area = re.findall('\d+', house_area)[0]
	    		# 房子的装修情况
	    		house_decoration = infos[4]
	    		# 房子的总价
	    		house_totalPrice = li.select('div.info.clear > div.priceInfo > div.totalPrice > span')[0].text
	    		# 房子的单价
	    		house_unitPrice = li.select('div.info.clear > div.priceInfo > div.unitPrice > span')[0].text
	    		house_unitPrice =  re.findall('\d+', house_unitPrice)[0]
	    		item['house_locaiton'] = house_locaiton
	    		item['house_type'] = house_type
	    		item['house_area'] = house_area
	    		item['house_decoration'] = house_decoration
	    		item['house_totalPrice'] = house_totalPrice
	    		item['house_unitPrice'] = house_unitPrice
	    		yield item
    	except Exception as e:
    		print e 

    	if self.next_page<=self.toal_page:
    		url = self.start_urls[0] + 'pg' + str(self.next_page) + '/'
    		self.next_page +=1
    		yield scrapy.Request(url, callback=self.parse)
 		


