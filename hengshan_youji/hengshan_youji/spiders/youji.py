import scrapy
from hengshan_youji.items import HengshanYoujiItem
import re

from  bs4 import BeautifulSoup

class YouJiSpider(scrapy.Spider):
    name = 'youji'
    allowed_domains = ['mafengwo.cn']
    start_urls = [
        'http://www.mafengwo.cn/yj/11886/']
    offset = 0
    totalPage = 0

    def parse(self, response):
        print('开始解析数据')
        soup = BeautifulSoup(response.text, "lxml")
        urls = soup.find_all('li' ,attrs={'class':'post-item clearfix'})

        for url in urls:
            a = url.find_all('a')[0]
            print (a['href'])
