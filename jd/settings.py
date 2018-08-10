# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
# Scrapy settings for jd project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jd'

SPIDER_MODULES = ['jd.spiders']
NEWSPIDER_MODULE = 'jd.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0(X11; Linux x86_64)AppleWebKit/537.36(KHTML,like Gecko)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Referer': 'https://search.jd.com/Search?keyword=%E5%8D%8E%E4%B8%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E5%8D%8E%E4%B8%BA&ev=exbrand_%E5%8D%8E%E4%B8%BA%EF%BC%88HUAWEI%EF%BC%89%5E&page=5&s=112&click=0'
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'jd.middlewares.JdSpiderMiddleware': 543,
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'jd.middlewares.JdDownloaderMiddleware': 543,
    'scrapy_splash.SplashMiddleware':725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware':810,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'jd.middlewares.ProxyPoolMiddleware': 700,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'jd.pipelines.JdPipeline': 300,
    'jd.pipelines.DetailPipeline':303,
    'jd.pipelines.HWPipeline':302,
    'jd.pipelines.DataClearPipeline':200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

SPLASH_URL = 'http://192.168.99.100:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

MYSQL_HOST = 'localhost'
PORT = 3306
USER = 'root'
PASSWORD = '123456'
DB = 'jd_huawei'

