# -*- coding: utf-8 -*-
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import pymysql
import pandas as pd


conn=pymysql.connect(host='localhost',user='root',password='Fzy520mm!',port=3306,db='lagou',charset='utf8')
sql="select * from analyst2"
data=pd.read_sql(sql,conn)

text=data["positionLables"].str.split(",").tolist()
text2=[i for j in text for i in j]
text3=str(text2)

# 中文分词
text4 = ' '.join(jieba.cut(text3))


# 生成对象
wc = WordCloud(font_path='/System/Library/Fonts/PingFang.ttc', width=800, height=600, mode='RGBA', collocations=False,background_color="white").generate(text4)

# 显示词云
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()

# 保存到文件
wc.to_file('./wordcloud.png')
