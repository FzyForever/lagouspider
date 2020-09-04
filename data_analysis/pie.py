# -*- coding: utf-8 -*-
from wordcloud import WordCloud
import matplotlib as mpl
from matplotlib import pyplot as plt
import pymysql
import pandas as pd
from matplotlib import font_manager

my_font=font_manager.FontProperties(fname="/System/Library/Fonts/PingFang.ttc")
conn=pymysql.connect(host='localhost',user='root',password='Fzy520mm!',port=3306,db='lagou',charset='utf8')
sql="select * from analyst2"
data=pd.read_sql(sql,conn)

text=list(data["education"])
df=pd.value_counts(text)
education=list(df.index)
num=list(df.values)
explode=[0,0.1,0,0.1]
plt.figure()
p=plt.pie(num,explode=explode,labels=education, autopct='%1.1f%%',
        shadow=True, startangle=90)
for front in p[1]:
    front.set_fontproperties(mpl.font_manager.FontProperties(
        fname='/System/Library/Fonts/PingFang.ttc'))
plt.title("数据分析师的学历要求",fontproperties=my_font)

plt.show()
plt.savefig("./数据分析师的学历要求.png")

