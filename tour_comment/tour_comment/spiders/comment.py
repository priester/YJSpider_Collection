import scrapy
from tour_comment.items import TourCommentItem
import re
from bs4 import BeautifulSoup



class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['tripadvisor.cn']
    start_urls = ['https://www.tripadvisor.cn/Attraction_Review-g679670-d505434-Reviews-Mount_Hengshan-Hengyang_Hunan.html']
    offset = 0
    totalPage = 0

    'https://www.tripadvisor.cn/Attraction_Review-g679670-d505434-Reviews-or10-Mount_Hengshan-Hengyang_Hunan.html'

    def parse(self, response):
        print('傻逼===========')
        soup = BeautifulSoup(response.text,"lxml")
        # print(soup.find_all('p',attrs={'class':'partial_entry'}))

        comments = soup.find_all('p',attrs={'class':'partial_entry'})
        for comment in comments[2:]:
            rets = re.findall(r'\w+',comment.text)
            ret = ''.join(rets)
            # print(ret)
            item = TourCommentItem()
            item['toure_comment'] = ret
            yield item
        totalPage = soup.find_all('a',attrs={'class':'pageNum last taLnk '})[0].text
        self.totalPage = int(totalPage)

        if self.totalPage > 0:
            self.offset +=10
            self.totalPage -=1
            url = 'https://www.tripadvisor.cn/Attraction_Review-g679670-d505434-Reviews-or' + str(self.offset) + '-Mount_Hengshan-Hengyang_Hunan.html'
            yield  scrapy.Request(url,callback=self.parse)


        # print(response.text)
