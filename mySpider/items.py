# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #id = scrapy.Field()
    _title = scrapy.Field()
    _content = scrapy.Field()
    _url = scrapy.Field()
    _source = scrapy.Field()
    _time = scrapy.Field()
