#coding:utf8

import redis
import json

REDIS_HOST = '127.0.0.1'
r = redis.Redis(host=REDIS_HOST)
base_url = 'https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?id={}&displayable-kind=11&startIndex=1&endIndex=15&sort=0'
'''
    STIME格式
    {'1234546': '2018-10-01'}
'''

STIME = json.loads(r.get('stime'))

for appid  in STIME.keys():
    url = base_url.format(appid)
    r.lpush('comment_spider:start_urls', url)



