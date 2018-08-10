# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import re
import logging
from jd.items import Hwphone
from jd.items import DetailItem
import pymysql



class DataClearPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,Hwphone):
            if item["detail_url"][0]  != 'h':
                item["detail_url"] = 'https:' + item['detail_url']
            return item
        elif isinstance(item,DetailItem):
            item["staging"] = re.sub('\'\s+?\'',' ',"""{}""".format(str(item["staging"])))
            item["color"] = re.sub('\'\s+?\'',' ',"""{}""".format(str(item["color"])))
            return item



class HWPipeline(object):
    def __init__(self,host,db,port,user,password):
        self.host = host
        self.db = db
        self.port = port
        self.user = user
        self.password = password
        pass

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get("MYSQL_HOST"),
            port = crawler.settings.get("PORT"),
            user = crawler.settings.get("USER"),
            password = crawler.settings.get("PASSWORD"),
            db = crawler.settings.get("DB")
        )

    def open_spider(self,spiser):
        self.client = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,db=self.db,charset='utf8')
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        if isinstance(item,Hwphone):
            d = dict(item)
            try:
                sql = 'insert into jd_huawei VALUES ("{}","{}","{}","{}","{}")'.format(d["title"],d["price"],d["shop_name"],d["comment_counts"],d["detail_url"],)
                self.cursor.execute(sql)
                self.client.commit()
            except Exception as e:
                print(e)
                logging.basicConfig(filename="log.txt")
                logging.warning(e)
                logging.error(e)
                logging.critical(e)
        return item

    def spider_closed(self, spider):
        self.client.close()

class DetailPipeline(object):
    def __init__(self,host,db,port,user,password):
        self.host = host
        self.db = db
        self.port = port
        self.user = user
        self.password = password

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get("MYSQL_HOST"),
            port = crawler.settings.get("PORT"),
            user = crawler.settings.get("USER"),
            password = crawler.settings.get("PASSWORD"),
            db = crawler.settings.get("DB")
        )

    def open_spider(self,spiser):
        self.client = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,db=self.db,charset='utf8')
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        # print(item)
        if isinstance(item,DetailItem):
            print("************")
            d = dict(item)
            print(d)
            try:
                sql = 'insert into jd_huawei_detail VALUES ("{}","{}","{}","{}","{}","{}","{}","{}")'.format(d["title"],d["color"],d["price"],d["promotion"],d["staging"],d["value_add"],d["value_add_promotion"],d["version"])
                self.cursor.execute(sql)
                self.client.commit()
            except Exception as e:
                print(e)
                logging.basicConfig(filename="log.txt")
                logging.warning(e)
                logging.error(e)
                logging.critical(e)
        return item

    def spider_closed(self, spider):
        self.client.close()

