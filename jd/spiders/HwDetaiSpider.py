# -*- coding: utf-8 -*-
import pymysql
import re
import scrapy
import time
from scrapy import Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
# from jd.items import Hwphone
# from jdjd.items import DetailItem
from jd.items import DetailItem
import sys
from urllib.parse import urlencode



class HwdetailspiderSpider(scrapy.Spider):
    name = 'HwDetailSpider'
    allowed_domains = ['item.jd.com']
    base_url = 'https://'
    MYSQL_HOST = 'localhost'
    PORT = 3306
    USER = 'root'
    PASSWORD = '123456'
    DB = 'jd_huawei'
    client = pymysql.connect(host=MYSQL_HOST, port=PORT, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cursor = client.cursor()
    # splash.images_enabled = false
    # splash.plugins_enabled = false

    script = """
        function main(splash)
            splash.images_enabled = false
            splash.plugins_enabled = false
            splash:go(splash.args.url)
            splash:wait(7)
            return splash:html()
        end
    """

    def start_requests(self):
        sql = 'SELECT detail_link FROM jd_huawei'
        self.cursor.execute(sql)
        link_list = self.cursor.fetchall()
        # print(link_list)
        for link in list(set(link_list)):
            url = link[0]
            time.sleep(2)
            # yield scrapy.Request(url=url,callback=self.parse)
            yield SplashRequest(url=url,endpoint='execute',callback=self.parse,splash_url='http://192.168.99.100:8050',
                                args={
                                    'wait':7,
                                    'lua_source':self.script
                                })

    def parse(self, response):
        # print(response.text)
        item = DetailItem()
        result = response.xpath('//div[@class="itemInfo-wrap"]')
        title = result.xpath("./div[@class='sku-name']/text()")
        if title:
            title = result.xpath("./div[@class='sku-name']/text()").extract()[0].strip()
        else:
            title = "NA"
        price_ = result.xpath(".//div[@class='summary-price-wrap']//div[@class='dd']/span[contains(@class,'p-price')]")
        if price_:
            price = price_.xpath("string(.)").extract()[0]
        else:
            price = "NA"
        value_add_ = result.xpath(".//li[@id='support-old2new']/a")
        if value_add_:
            value_add = value_add_.xpath("string(.)").extract()[0].strip()
        else:
            value_add = "NA"
        value_add_promotion_ = result.xpath(".//div[contains(@class,'yb-item-cat')]/div[contains(@class,'yb-item')]")
        if value_add_promotion_:
            value_add_promotion = value_add_promotion_.xpath("string(.)").extract()[0].strip()
            # value_add_promotion = re.sub('\s+'," ",value_add_promotion)
        else:
            value_add_promotion = "NA"
        staging_ = result.xpath(".//div[contains(@class,'baitiao-list J-baitiao-list')]")
        if staging_:
            staging = re.sub('\s+'," ",staging_.xpath("string(.)").extract()[0].strip())
        else:
            staging = "NA"
        promotion_ = result.xpath(".//a[contains(@class,'notice')]")
        if promotion_:
            promotion = promotion_.xpath("string(.)").extract()[0].strip()
        else:
            promotion = "NA"
        color = response.xpath("//div[@id='choose-attr-1']/div[contains(@class,'dd')]/div/@title")
        if len(color) == 0:
            color = "NA"
        else:
            color_ = ""
            for i in color:
                color_ = color_ + i.extract() + " "
            color = color_
        version = response.xpath('//div[@id="choose-attr-2"]/div[@class="dd"]/div/@title')
        if len(version) == 0:
            version = "NA"
        else:
            version_ = ""
            for i in version:
                version_ = version_ + i.extract() + " "
                version = version_
        L = [title,version,price,color,value_add,value_add_promotion,staging,promotion]
        L_ = ['title','version','price','color','value_add','value_add_promotion','staging','promotion']
        for i in range(len(L)):
            item[L_[i]] = L[i]
        # print(item)
        yield item

# class HWdetailspiderSpider(scrapy.Spider):
#     name = 'HwDetailSpider'
#     allowed_domains = ['item.jd.com']
#     base_url = 'https://'
#     MYSQL_HOST = 'localhost'
#     PORT = 3306
#     USER = 'root'
#     PASSWORD = '123456'
#     DB = 'jd_huawei'
#     client = pymysql.connect(host=MYSQL_HOST, port=PORT, user=USER, password=PASSWORD, db=DB, charset='utf8')
#     cursor = client.cursor
#
#     def start_requests(self):
#         sql = 'SELECT detail_link FROM jd_huawei'
#         self.cursor.execute(sql)
#     #     link_list = self.cursor.fetchall()
#     #     print(link_list)
#     # #     for link in link_list:
#     #         url = link[0]
#     #         time.sleep(2)
#     #         yield scrapy.Request(url=url,callback=self.parse)
#     #
#     # def parse(self, response):
#     #     print(response.text)








