import scrapy
class Lagou1Item(scrapy.Item):
    positionId=scrapy.Field()
    positionName=scrapy.Field()
    education=scrapy.Field()
    createTime=scrapy.Field()
    companyId=scrapy.Field()
    companyShortName=scrapy.Field()
    companyFullName=scrapy.Field()
    city=scrapy.Field()
    salary=scrapy.Field()
    positionLables=scrapy.Field()
    job_detail_url=scrapy.Field()
    workYear=scrapy.Field()






