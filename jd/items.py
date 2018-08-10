# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Hwphone(scrapy.Item):
    price = scrapy.Field()
    detail_url = scrapy.Field()
    shop_name = scrapy.Field()
    comment_counts = scrapy.Field()
    title = scrapy.Field()

class DetailItem(scrapy.Item):
    title =scrapy.Field()
    #单价
    price = scrapy.Field()
    #促销
    promotion = scrapy.Field()
    #增值业务
    value_add = scrapy.Field()
    #选择颜色
    color = scrapy.Field()
    #选择版本
    version = scrapy.Field()
    #增值保障
    value_add_promotion = scrapy.Field()
    #白天分期
    staging = scrapy.Field()
    # post_view_count = scrapy.Field()
    # post_comment_count = scrapy.Field()
    # url = scrapy.Field()

