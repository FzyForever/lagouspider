# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from lagou1.items import Lagou1Item
import json
import requests
import scrapy
import time
from bs4 import BeautifulSoup


class LagouspiderSpider(RedisSpider):
    name = 'lagouspider'
    allowed_domains = ['lagou.com']
    redis_key ="lagou"
    # start_urls = [
    #     'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false']  # 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'


    # def start_requests(self):
    #     for i in range(1, 30):
    #
    #         yield scrapy.FormRequest(self.start_urls[0], headers=self.h3, formdata=para,
    #                                  cookies=self.get_Cookies(self.proxies, self.h1),
    #                                  callback=self.parse)  # 也可以使用如下的request,不过结果不同？？？
         #yield scrapy.Request(self.start_urls[0],method="POST",headers=self.h3,body=json.dumps(para),cookies=self.cookies,callback=self.parse) #功能同上条Formrequest，不过要增加method参数，formdata改成body，且接受json数据



    def make_request_from_data(self,data):
        """Returns a Request instance from data coming from Redis.
        By default, ``data`` is an encoded URL. You can override this method to
        provide your own message decoding.
        Parameters
        ----------
        data : bytes
         Message from redis.
        """
        data = json.loads(data)
        url = data.get('url')
        form_data = data.get('form_data')
        headers=data.get("headers")
        cookies=data.get("cookies")
        return scrapy.FormRequest(url=url,formdata=form_data,headers=headers,cookies=cookies,callback=self.parse)


    def parse(self,response):
        item = Lagou1Item()
        t = json.loads(response.body_as_unicode())  # 注意loads函数的使用
        positionId_list = []
        positionName_list = []
        createTime_list = []
        companyId_list = []
        companyShortName_list = []
        companyFullName_list = []
        city_list = []
        salary_list = []
        positionLables_list = []
        education_list=[]
        job_detail_url_list = []
        workYear_list=[]

        for results in t['content']['positionResult']['result']:
            positionId = results['positionId']
            positionName = results['positionName']
            createTime = results['createTime']
            companyShortName = results['companyShortName']
            #            workYear = results['workYear']
            city = results['city']
            education=results["education"]
            workYear=results["workYear"]
            salary = results['salary']
            companyId = results['companyId']
            companyFullName = results['companyFullName']
            positionLables = results['positionLables']
            positionLables = ','.join(positionLables)
            #            positionAdvantage = results['positionAdvantage']
            job_detail_url = 'https://www.lagou.com/jobs/' + str(positionId) + '.html'
            #            companyLogo=results['companyLogo']
            #            print(positionName,companyShortName,workYear,city,salary,positionLables,positionAdvantage,companyLogo) #查看是否顺利爬取数据
            positionId_list.append(positionId)
            positionName_list.append(positionName)
            createTime_list.append(createTime)
            companyId_list.append(companyId)
            companyShortName_list.append(companyShortName)
            companyFullName_list.append(companyFullName)
            positionLables_list.append(positionLables)
            city_list.append(city)
            salary_list.append(salary)
            job_detail_url_list.append(job_detail_url)
            education_list.append(education)
            workYear_list.append(workYear)
        item['positionId'] = positionId_list
        item['positionName'] = positionName_list
        item['createTime'] = createTime_list
        item['companyShortName'] = companyShortName_list
        item['companyFullName'] = companyFullName_list
        item['city'] = city_list
        item['companyId'] = companyId_list
        item['salary'] = salary_list
        item['positionLables'] = positionLables_list
        item['job_detail_url'] = job_detail_url_list
        item["education"]=education_list
        item["workYear"]=workYear_list
        yield item
        #返回岗位基本信息供pipeline入库。
        # for i in item['job_detail_url']:  # 请求岗位详细信息url，回调函数parse_job_detail继续解析
        #     yield scrapy.Request(i, headers=self.h4, cookies=self.get_Cookies(self.proxies, self.h4),
        #                          callback=self.parse_job_details)  # 此处cookies很重要，否则反爬起作用，得不到结果

    #
    #
    # def parse_job_details(self, response):  # 用来获取详细的职位描述，以及职位编号，用来和parse函数获取的信息进行匹配。
    #     # soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
    #     item = Lagou1Item()
    #     positionId = response.url.split('/')[-1].split('.')[0].strip()
    #     #        job_trigger=response.xpath('//*[@id="job_detail"]/dd[1]/p/text()').extract()
    #     #        job_description =response.xpath('//*[@id="job_detail"]/dd[2]/div/text()').extract().strip()
    #     # try:  # beatifulsoup解析
    #     #     job_trigger = soup.select_one('#job_detail > dd.job-advantage >p').text.strip()
    #     #     job_description = soup.select_one('#job_detail > dd.job_bt > div').text.strip()
    #     # except Exception as e:
    #     #     print(e)
    #     # 以下是测试时面临反爬，无法得到结果时尝试的xpath方式，后来解决反爬的为，也就用不到了。
    #     job_description=response.xpath('//*@id="job_detail"]/dd[2]/div/text()').extract()
    #     job_trigger=response.xpath('//*[@id="job_detail"]/dd[1]/p/text()').extract()
    #     job_description=''.join(job_description)
    #     job_trigger=''.join(job_trigger)
    #     item['positionId'] = positionId
    #     item['job_description'] = job_description
    #     item['job_trigger'] = job_trigger
    #     return item
