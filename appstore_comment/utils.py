#coding:utf8
import urlparse
import datetime

def get_parsed_qs_from_url(url):
    '''
        获取解析成字典的qs

        input: 
            http://www.baidu.com/?a=1&b=2

        output:
            {'a':'1', 'b':'2'}
    '''
    qs = urlparse.urlparse(url).query
    return {k: v for k, v in urlparse.parse_qsl(qs)}


def utctime_to_localtime(utctime, tz=8):
    if isinstance(utctime, str):
        utctime = utctime.decode('utf8')
    
    if isinstance(utctime, unicode):
        utctime = datetime.datetime.strptime(utctime,'%Y-%m-%dT%H:%M:%SZ')

    return utctime + datetime.timedelta(hours=tz)
