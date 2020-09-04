BOT_NAME = 'lagou1'
SPIDER_MODULES = ['lagou1.spiders']
NEWSPIDER_MODULE = 'lagou1.spiders'
MYSQL_CONNECTION='mysql+pymysql://root:Fzy520mm!@localhost:3306/lagou?charset=utf8'

#scrapy_redis
SCHEDULER ="scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS ="scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True

REDIS_URL = "redis://127.0.0.1:6379"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False #这个改成True，经常会没有结果。
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 2
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 3
CONCURRENT_REQUESTS_PER_IP = 3
# Disable cookies (enabled by default)
COOKIES_ENABLED = True
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
}
DOWNLOADER_MIDDLEWARES = {
    'lagou1.middlewares.Lagou1DownloaderMiddleware': 400,
#    'lagou1.middlewares.CustomerMiddleware':200
}
MEDIA_ALLOW_REDIRECTS =True #^^^^^^^^^^^^^^^^^^^^^^重要，解决图片无法下载
ITEM_PIPELINES = {
      'lagou1.pipelines.Lagou1Pipeline': 300,
    #'lagou1.pipelines.Lagou1Pipeline2': 310,
#    'lagou1.pipelines.DownloadFile':320,
}
