# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from appstore_comment.items import AppstoreCommentItem

class CommentSpider(RedisCrawlSpider):
    name = 'comment_spider'
    allowed_domains = ['itunes.apple.com']
    redis_key = 'comment_spider:start_urls'

    def parse(self, response):
        item = AppstoreCommentItem()
        item['url'] = url
        item['body'] = response.body
        return response
