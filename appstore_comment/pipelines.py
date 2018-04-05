# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class AppstoreCommentPipeline(object):
    def process_item(self, item, spider):
        url  = item['url']
        body = item['body']
        try:
            jdata = json.loads(body)
        except Exception as e:
            spider.log.error(e.message)
        '''
            处理评论数据
        '''
        reviews = jdata['userReviewList']
        return item

