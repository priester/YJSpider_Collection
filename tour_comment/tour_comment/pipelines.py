# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TourCommentPipeline(object):
    def process_item(self, item, spider):
        print('我被调用了')
        with open('./comments.txt','a') as fp:

            fp.write(item['toure_comment'] + '\n')
        return item


