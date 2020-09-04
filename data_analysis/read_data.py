import pandas as pd
import pymysql
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import font_manager

conn=pymysql.connect(host='localhost',user='root',password='Fzy520mm!',port=3306,db='lagou',charset='utf8')
sql="select * from analyst2"
data=pd.read_sql(sql,conn)
my_font=font_manager.FontProperties(fname="/System/Library/Fonts/PingFang.ttc")
index=list(data.columns)
# print(index)


#删除不需要的列
x=[0,1,3,4]
df=data.drop(data.columns[x],axis=1)


def unitchange(salary):
    if salary.find("k") != -1:
        salary =int(salary.split("k")[0])*1000
    else:
        salary = np.nan
    return salary


# 对salary进行处理，转化为整型，方便计算
df['salary_range'] = df['salary'].str.split("-")
df['min_salary'] = df['salary_range'].str.get(0)
df['max_salary'] = df['salary_range'].str.get(1)
df['min_salary'] = df['min_salary'].map(unitchange)
df['max_salary'] = df['max_salary'].fillna('unknown').map(unitchange)

#计算得到平均工资
average_salary=(df['max_salary'].mean()+df['min_salary'].mean())/2
df['average_salary']=(df['max_salary']+df['min_salary'])/2
df.drop(['min_salary','max_salary','salary'],axis=1,inplace=True)

#工资水平与工作年限的关系
ex_sa=df.groupby(df['workYear']).mean().sort_values(by='average_salary')

#设置图片大小
plt.figure(figsize=(20,8),dpi=80)

_x=ex_sa.index
_y=ex_sa.values.astype(int)
_y=[i for j in _y for i in j]

#画图
plt.bar(range(len(_x)),_y,color="orange",label="平均工资")

#设置x轴的刻度
plt.xticks(range(len(_x)),_x,fontproperties=my_font)

#给图片添加描述
plt.xlabel("工作年限",fontproperties=my_font)
plt.ylabel("工资水平",fontproperties=my_font)
plt.title("工资水平与工作年限的关系",fontproperties=my_font)

#添加图例
plt.legend(prop=my_font,loc="best")

#添加网格
plt.grid(alpha=0.3)

#保存图片
plt.savefig("./工资水平与工作年限的关系.png")






#工资与学历的关系
edu_sa=df.groupby(df['city']).mean().sort_values(by='average_salary',ascending=False)[:15]

#设置图片大小
plt.figure(figsize=(20,8),dpi=80)

_x2=edu_sa.index
_y2=edu_sa.values.astype(int)
_y2=[i for j in _y2 for i in j]

#画图
plt.bar(range(len(_x2)),_y2,color="green",label="平均工资")

#设置x轴的刻度
plt.xticks(range(len(_x2)),_x2,fontproperties=my_font)

#给图片添加描述
plt.xlabel("城市",fontproperties=my_font)
plt.ylabel("工资水平",fontproperties=my_font)
plt.title("平均工资与城市的关系",fontproperties=my_font)

#添加图例
plt.legend(prop=my_font,loc="best")

#添加网格
plt.grid(alpha=0.3)

#保存图片
plt.savefig("./工资水平与城市关系.png")








