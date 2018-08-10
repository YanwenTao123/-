# -*- coding: utf-8 -*-
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
from jd.items import Hwphone
from jd.items import DetailItem
import sys
from urllib.parse import urlencode


class JdspiderSpider(scrapy.Spider):
    name = 'jdSpider'
    allowed_domains = ['search.jd.com']
    base_url = 'https://search.jd.com/Search?'
    script = """
        function main(splash)
            splash:go(splash.args.url)
            splash:wait(2)
            splash:evaljs("document.getElementsByClassName('p-num')[0].scrollIntoView(true)")
            splash:wait(2)
            return splash:html()
        end
    """
    script_detail = """
        function main(splash)
            splash:go(splash.args.url)
            splash:wait(2)
            return splash:html()
    """

    def start_requests(self):
        for i in range(1,10,2):
            url = self.base_url +'keyword='+'华为手机'+'&enc=utf-8&wq='+"华为手机" #+'&page=' +str(i)
            # print(url)
            time.sleep(1)
            yield SplashRequest(url=url+'&page='+str(i),callback=self.parse,args={
                'lua_source':self.script,
                "page":i,
                "wait":3,
            },endpoint="execute",splash_url='http://192.168.99.100:8050')

    def parse(self, response):
        result = response
        # result = result.css('html').extract()
        ul = result.xpath('//div[@id="J_goodsList"]/ul/li')
        # good_list = []

        good_dict = Hwphone()
        for i in ul:
            price = i.xpath('.//div[@class="p-price"]//i/text()')[0].extract()
            comment_counts = i.xpath('.//div[@class="p-commit"]/strong/a/text()')[0].extract()
            title = ' '.join(i.xpath('./div[contains(@class,p-name)]//em/text()')[1:].extract())
            shop_name = i.xpath('.//div[@class="p-shop"]//a/@title').extract()
            if not shop_name:
                shop_name = "NA"
            else:
                shop_name = i.xpath('.//div[@class="p-shop"]//a/@title')[0].extract()
            detail_link = i.xpath('.//div[@class="p-img"]/a/@href')[0].extract()
            l = ["price", "comment_counts", "title", "shop_name", "detail_url"]
            l_1 = [price, comment_counts, title, shop_name, detail_link]
            for j in range(len(l)):
                good_dict[l[j]] = l_1[j]
            # print(good_dict)
            # yield SplashRequest(url='https:'+detail_link,callback=self.detail_parse,args={'lua_source':self.script_detail},endpoint='execute',splash_url='http://192.168.99.100:8050')
            yield good_dict

    def detail_parse(self,response):
        print("**************************")
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
            staging = re.sub('\s+', " ", staging_.xpath("string(.)").extract()[0].strip())
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
        L = [title, version, price, color, value_add, value_add_promotion, staging, promotion]
        L_ = ['title', 'version', 'price', 'color', 'value_add', 'value_add_promotion', 'staging', 'promotion']
        for i in range(len(L)):
            item[L_[i]] = L[i]
        # print(item)
        yield item


