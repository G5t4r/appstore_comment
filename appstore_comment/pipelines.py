# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import redis
import datetime
import time
import traceback

from appstore_comment.settings import REDIS_HOST
from appstore_comment.utils import utctime_to_localtime, get_parsed_qs_from_url


base_url = 'https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?id={}&displayable-kind=11&startIndex={}&endIndex={}&sort=0'

class AppstoreCommentPipeline(object):

    def process_item(self, item, spider):
        url = item['url']
        reviews = item['reviews']
        s_time =  item['s_time']
        start_index = int(item['url_qs'].get('startIndex'))
        end_index = int(item['url_qs'].get('endIndex'))
        appid = item['url_qs'].get('id')
        delta = 200
        continue_crawl = True
        

        cleaned_reviews = []
        for raw_review in reviews:
            post_time = utctime_to_localtime(raw_review['date'])
            if post_time > s_time:
                review = {}
                review['create_time'] = int(time.time())
                review['date'] = post_time.strftime('%Y-%m-%d %H:%M:%S')
                review['title'] = raw_review['title']
                review['body'] = raw_review['body']
                review['name'] = raw_review['name']
                review['rating'] = raw_review['rating']
                review['userReviewId'] = raw_review['userReviewId']
                cleaned_reviews.append(json.dumps(review))
            else:
                continue_crawl = False
                break

        spider.redis_db.lpush('itunes_review_applist', *cleaned_reviews)

        if continue_crawl:
            start_index, end_index = end_index, (end_index+200)
            next_url = base_url.format(appid, start_index, end_index)
            spider.redis_db.lpush('comment_spider:start_urls', next_url)

        return item
