# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Lagoujob(Base):  # 这个参数父类名
    __tablename__ = 'analyst3'  # 存储岗位基本信息的数据表
    id = Column(Integer, primary_key=True)
    positionId = Column(String(50), unique=True)
    positionName = Column(String(50))
    createTime = Column(DateTime)
    companyId = Column(String(50))
    education=Column(String(10))
    workYear=Column(String(50))
    companyShortName = Column(String(100))
    companyFullName = Column(String(100))  # 公司简称的长度超过想象，所以数值要大些
    city = Column(String(50))
    salary = Column(String(30))
    positionLables = Column(String(100))
    job_detail_url = Column(String(100))



# class Lagoudetails(Base):
#     __tablename__ = 'lagoudetails'  # 存储岗位详细信息的数据表
#     id = Column(Integer, primary_key=True)
#     positionId = Column(String(50), unique=True)
#     job_trigger = Column(String(100))
#     job_description = Column(String(1000))


class Lagou1Pipeline(object):
    def __init__(self):
        connection = 'mysql+pymysql://root:xxxxxxx@localhost:3306/lagou?charset=utf8'  # UTF8MB4
        engine = create_engine(connection, echo=True)  # 数据库连接
        DBSession = sessionmaker(bind=engine)  # 创建会话对象，用于数据表的操作
        self.Sqlsession = DBSession()
        Base.metadata.create_all(engine)  # 创建数据表

    def process_item(self, item, spider):
        if 'job_trigger' not in item.keys():  #两个pipeline处理
            for i in range(0, len(item['positionId'])):  # 这里不能用len(item)，因为只有10个字段，只能存入前10条记录
                try:
                    jobs = Lagoujob(positionId=item['positionId'][i], positionName=item['positionName'][i],
                                    education=item["education"][i],
                                    workYear=item["workYear"][i],
                                    createTime=item['createTime'][i],
                                    companyId=item['companyId'][i],
                                    companyShortName=item['companyShortName'][i],
                                    companyFullName=item['companyFullName'][i],
                                    city=item['city'][i],
                                    salary=item['salary'][i],
                                    positionLables=item['positionLables'][i],
                                    job_detail_url=item['job_detail_url'][i])
                    self.Sqlsession.add(jobs)
                    self.Sqlsession.commit()
                except Exception as e:
                    self.Sqlsession.rollback()  # 如果需要执行异常语句，此句不可少!
                    #                    pass
                    print(e)

        return item


# # 以下需要另外做一个类
# class Lagou1Pipeline2(object):
#     def __init__(self):
#         connection = 'mysql+pymysql://root:Fzy520mm!@localhost:3306/lagou?charset=utf8'  # UTF8MB4
#         engine = create_engine(connection, echo=True)  # 数据库连接
#         DBSession = sessionmaker(bind=engine)  # 创建会话对象，用于数据表的操作
#         self.Sqlsession2 = DBSession()
#         Base.metadata.create_all(engine)  # 创建数据表
#
#     def process_item(self, item, spider):
#         if 'job_trigger' in item:
#             jobdetails = Lagoudetails(positionId=item['positionId'],
#                                      job_trigger=item['job_trigger'],
#                                      job_description=item['job_description'])
#             try:
#                 self.Sqlsession2.add(jobdetails)
#                 self.Sqlsession2.commit()
#             except Exception as e:
#                 print(e)
#
#     #                self.Sqlsession2.rollback()
#         return item


class DownloadFile(ImagesPipeline):  # 爬取图片pipeline未使用。
    def get_media_requests(self, item, info):
        for url, filename in zip(item['FileUrl'], item['FileName']):
            cookies = {'X_HTTP_TOKEN': '42daf4b72327b2815637417751bf5e71415983ed09',
                       'user_trace_token': '20191224082925-308fab45-3629-4198-be34-cbb2eb78a270',
                       'JSESSIONID': 'ABAAABAAAGGABCB228791B35A6AD371A8A3D1C8FF1D6C88',
                       'SEARCH_ID': 'fd50d5fe208f4940a22a2bd69d76a576'}
            h3 = {'User-Agent': 'Opera/9.80 (iPhone; Opera Mini/7.1.32694/27.1407; U; en) Presto/2.8.119 Version/11.10', \
                  'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='}
            yield Request(url, headers=h3, cookies=cookies, meta={'name': filename})

    def file_path(self, request, response=None, info=None):
        file_name = 'E:\\scrapypro\\lagou1\\pic\\' + (request.meta['name']) + '.jpg'
        return file_name

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path
        return item

