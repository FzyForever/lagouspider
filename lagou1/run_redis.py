import redis
import json
import requests

rd = redis.Redis('127.0.0.1', port=6379)
h1={'User-Agent': 'Opera/9.80 (iPhone; Opera Mini/7.1.32694/27.1407; U; en) Presto/2.8.119 Version/11.10',\
'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='} #创建不同的headers
h2={'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17',\
'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='}
h3={'User-Agent': 'Opera/9.80 (iPhone; Opera Mini/7.1.32694/27.1407; U; en) Presto/2.8.119 Version/11.10',\
'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='}
h4={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}


def get_Cookies(proxies,headers): #构建获得cookies的函数
    url = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88?'
    session = requests.session()
    session.post(url,headers=headers,proxies=proxies)
    cookies = session.cookies
    return cookies.get_dict()

def push_start_url_data(request_data):
    rd.lpush('lagou', request_data)

if __name__ == '__main__':
    url ="https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
    cookie = get_Cookies(proxies, h1)
    for i in range(30):
        form_data={'first': 'true', 'pn':str(i), 'kd': '数据分析师'}
        request_data = {
            "url":url,
            "form_data":form_data,
            "cookies":cookie,
            "headers":h3
        }
        push_start_url_data(json.dumps(request_data))


