# -*- coding: utf-8 -*-
import scrapy
from cs_house.items import CsHouseItem
from bs4 import BeautifulSoup
class CsLoupanSpider(scrapy.Spider):
    name = 'cs_loupan'
    allowed_domains = ['cs.fang.lianjia.com']
    start_urls = ['https://cs.fang.lianjia.com/loupan/']
    next_page = 2
    total_page = 50

    def parse(self, response):
    	soup = BeautifulSoup(response.text,'html.parser')
    	print soup.title.text
    	print "========================开始=================="
    	list_wraps = soup.find_all(name='ul', class_='house-lst', recursive=True, text=None, limit=None)
    	print list_wraps
    	print "========================结束=================="
    	
    	for li in list_wraps[0].find_all(name='li',attrs={'data-index':'0'}):
    		#house-lst > li:nth-child(1) > div.info-panel > div.col-1 > h2
    		# print li.find_all('a',data-el='xinfang')[0].text
    		# print li.text
    		print '--------------------'
    		try:
    			# 1.楼盘名字
	    		houseTitles = li.select('div.info-panel > div.col-1 > h2 > a')
	    		loupan_title = ''
	    		if len(houseTitles):
	    			loupan_title = houseTitles[0].text
	    			print 'loupan_title:' + loupan_title
	    		# 2.楼盘均价
	    		average_price = li.select('div.info-panel > div.col-2 > div > div > span')[0].text
	    		print 'average_price:' + average_price
	    		# 3.楼盘所在区域
	    		loupan_region = li.select('div.info-panel > div.col-1 > div.where > span')[0].text.split('-')[0]
	    		print 'loupan_region:' + loupan_region
	    		# 4.楼盘的具体地址
	    		loupan_detailAddress = li.select('div.info-panel > div.col-1 > div.where > span')[0].text
	    		print 'loupan_detailAddress:' + loupan_detailAddress
	    		# 5.楼盘的类型
	    		loupan_type = li.select('div.info-panel > div.col-1 > div.type > span.live')[0].text
	    		print 'loupan_type:' + loupan_type
	    		item = CsHouseItem()
	    		item['loupan_title'] = loupan_title
	    		item['average_price'] = average_price
	    		item['loupan_region'] = loupan_region
	    		item['loupan_detailAddress'] = loupan_detailAddress
	    		item['loupan_type'] = loupan_type
	    		yield item
	    	except Exception as e:
	    		print e

    		
    	# 找打页面信息
    	page_box = soup.find_all('div',class_='page-box house-lst-page-box')[0]
    	print page_box
    	page_list = page_box.find_all('a')
    	print page_list
    	# next_page = page_list[-1]
    	if self.next_page<=self.total_page:
    		url = self.start_urls[0] + 'pg' + str(self.next_page) + '/'
    		self.next_page+=1 
    		yield scrapy.Request(url, callback=self.parse)
    		

    	

    			

    	

