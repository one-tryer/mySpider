# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from mySpider.items import MyspiderItem
import time as ti
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider, RedisSpider
from ..utils import md5
import redis
import time as ti


class ChinanewsSpider(RedisCrawlSpider):

    name = 'chinanews'
    allowed_domains = ['chinanews.com']
    redis_key = "mySpider:start_urls"

    def __init__(self, *args, **kwargs):
        super(ChinanewsSpider, self).__init__(*args, **kwargs)
        try:
            r_t = redis.Redis(host='127.0.0.1', port=6379, db=0)
            # 目前关键词是自贸区，关键词是url中的q=
            base_url = 'http://sou.chinanews.com/search.do?q=%E8%87%AA%E8%B4%B8%E5%8C%BA&ps=10&start='
            # 设置中国新闻网读取页面数目
            for i in range(1, 10):
                url = base_url + \
                    str(i*10-10) + "&sort=pubtime&time_scope=0&channel=all&adv=1"
                r_t.lpush('mySpider:start_urls', url)
        except Exception as e:
            print("ChinanewsSpider__init__ false :")
            print(e)
            ti.sleep(5)

    # 获取每一条新闻
    content_links = LinkExtractor(
        allow=(r"http://www.chinanews.com/.*"), restrict_xpaths=('//a[@href]'))
    rules = (
        Rule(content_links, callback='parse2', follow=False),
    )

    def parse2(slef, response):
        try:
            item = MyspiderItem()
            item['_url'] = response.request.url
            #item['id'] = md5(response.request.url)
            item['_title'] = response.xpath(
                '//div[@id="cont_1_1_2"]/h1/text()')[0].extract().replace('\r\n', '').strip()
            contents = response.xpath(
                '//div[@class="left_zw"]/p/text()').extract()
            temp = ''
            for content in contents:
                temp += content.replace('\u3000', '').strip()
            item['_content'] = temp
            ti_and_src = response.xpath(
                '//div[@class="left-t"]/text()')[0].extract().replace('\u3000', ' ').strip().split(' ')
            item['_time'] = ti_and_src[0] + ti_and_src[1]
            item['_source'] = ti_and_src[2]
            yield item
        except Exception as e:
            print("ChinanewsSpider parse2 false :")
            print(e)
            ti.sleep(5)
