# -*- coding: utf-8 -*-
import redis
import traceback
import json
import datetime

from scrapy_redis.spiders import RedisCrawlSpider
from appstore_comment.settings import REDIS_HOST
from appstore_comment.items import AppstoreCommentItem
from appstore_comment.utils import get_parsed_qs_from_url, utctime_to_localtime

class CommentSpider(RedisCrawlSpider):
    name = 'comment_spider'
    allowed_domains = ['itunes.apple.com']
    redis_key = 'comment_spider:start_urls'
    redis_db = redis.Redis(host=REDIS_HOST)

    def parse(self, response):
        item = AppstoreCommentItem()

        try:
            jdata = json.loads(response.body)
        except Exception as e:
            traceback.print_exc()
            return None

        reviews = jdata['userReviewList']
        
        if len(reviews) == 0:
            return None

        qs = get_parsed_qs_from_url(response.url)
        appid = qs.get('id')

        try:
            STIME = json.loads(self.redis_db.get('stime'))
        except Exception as e:
            traceback.print_exc()
            return None

        if not appid:
            return None

        s_time= datetime.datetime.strptime(STIME[appid], '%Y-%m-%d')
        the_first_review_post_time = utctime_to_localtime(reviews[0]['date'])

        if the_first_review_post_time < s_time:
            return None
         
        item['url'] = response.url
        item['reviews'] = reviews
        item['url_qs'] = qs
        item['s_time'] = s_time

        return item
