# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy_redis.pipelines import RedisPipeline, default_serialize
from dao.mysql_helper import MySQLHelper
import time as ti


class MyspiderPipeline(RedisPipeline):

    def __init__(self, server,
                 key = SCHEDULER_DUPEFILTER_KEY,
                 serialize_func = default_serialize):
        super().__init__(server, key, serialize_func)
        
        #应该是这样
        self.my_sql = MySQLHelper()


    def process_item(self, item, spider):
        
        try:
            #insert_ok = my_sql.insert_news(item)
            my_sql.insert_news(item)
        except Exception as e:
            print("insert news to mysql is false in spider pipelines :")
            print(e)
            ti.sleep(5)
        return item
