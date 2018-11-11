# -*- coding: utf-8 -*-
'''
Created on 2018年11月10日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd 
import nltk
import codecs
all_data=pd.read_csv(r'./goods_comments_comment.csv')#读入总数据
print(all_data.head())
apple_data=all_data[all_data['手机品牌']=='苹果']#关于苹果的所有数据
huawei_data=all_data[all_data['手机品牌']=='华为']#关于华为的所有数据
xiaomi_data=all_data[all_data['手机品牌']=='小米']#关于小米的所有数据
# f=codecs.open('apple.txt','a','utf-8') #关于苹果的评论文件
# for i in apple_data['comment']:
#     f.write(str(i)+'/n')
# f=codecs.open('huawei.txt','a','utf-8') #关于华为的评论文件
# for i in huawei_data['comment']:
#     f.write(str(i)+'/n')    
f=codecs.open('xiaomi.txt','a','utf-8') 
for i in xiaomi_data['comment']:
    f.write(str(i)+'/n')
