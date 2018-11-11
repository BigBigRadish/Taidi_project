# -*- coding: utf-8 -*-
'''
Created on 2018年11月10日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import requests
import logging 
import urllib.request;
import time
import random
import json
import re
import urllib.request
import redis
import pymysql 
import itertools
from pymongo import MongoClient
from http import cookiejar
from nltk.ccg.lexicon import COMMENTS_RE
user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers={'User-Agent':user_agent}
requests.adapters.DEFAULT_RETRIES = 5
import re
def crawl_good_detail(i,collection):
    Url='http://gzjs.bazhuayu.com/?pageIndex='+str(i)#i一共有90页
    html=requests.get(Url);
    soup=BeautifulSoup(html.content,"lxml",from_encoding='utf-8')
    item=soup.findAll(class_='item')
    #n=0
    for i in item:
        #n+=1
        #print('正在爬取第'+str(n)+'个商品')
        goods_href=i.find('a').get('href')#获取商品url链接
        current_price=i.find(class_='number').text#获取商品价格
        #print(goods_href,price)
        good_name=i.find(class_='phone-name').text#获取商品名
        mobile_name=good_name.split(' ')[0]#手机品牌
        print(mobile_name)
        phone_shop=str(i.find(class_='shop').text)#获取商店信息
        if phone_shop==None:
            phone_shop='无'
        #print(goods_href)
        id=re.findall(r'\d+',str(goods_href))[0]#商品id
        #print(str(id))
        url_detail='http://gzjs.bazhuayu.com/detail/'+id#商品详情链接
        url_comment='http://gzjs.bazhuayu.com/comment/'+id#商品评论链接
        html1=requests.get(url_detail,headers=headers,verify=False);
        logging.captureWarnings(True)
        _cookies=html1.cookies#获取cookie
        soup1=BeautifulSoup(html1.content,"lxml",from_encoding='utf-8')
        #phone_name=soup1.find(class_='item disable').text#手机名
        attraction_title=soup1.find(style="font-size: 12px;color:#df3033;margin-bottom:10px;").text#吸引力标题
        if attraction_title==None:
            attraction_title='无'
        #print(attraction_title)
        if(soup1.find(style="color: #CCC;font-size: 10px;margin-left: 20px;text-decoration:line-through;")!=None):
            previous_price=soup1.find(style="color: #CCC;font-size: 10px;margin-left: 20px;text-decoration:line-through;").text
            print(previous_price)#原始价格
        else:
            previous_price=0#没有数据则用0填充
    #     turn_up=soup1.find(style="color: #666;font-size: 10px;margin-left: 10px;")#优惠情况，都有这个标签，不需要爬取
    #     if turn_up!=None:
    #         if turn_up.findAll('em')!=None:
    #             turn_up1=turn_up.findAll('em')[0].text#优惠情况1
    #             turn_up2=turn_up.findAll('em')[1].text#优惠情况1
    #         else:
    #             turn_up1='无'
    #             turn_up2='无'
        #transport_advices=soup1.findAll(class_="tag" )#运送和提示，由于所有商品都有，就不爬取了
                
        comment_condition=soup1.find(title="已忽略对购买帮助不大的评价" ).text
        #print(comment_condition)    
        comment_sum=re.findall(r'\d+',str(comment_condition))[0]#评论数量
        #print(str(comment_sum))      
        goods_detail=soup1.find(style="margin: 30px 88px;")#商品详情
        para_info=soup1.findAll(class_='info')#参数信息
        paras=''#详细参数
        if para_info!=None:
            for para in para_info:
                for i in para.findAll('span'):
                    paras+=i.text+','
        #print(paras)
        goods_detail1=goods_detail.findAll(class_="desc")#详细商品信息
        if goods_detail1==None:
            goods_detail1='无'
        goods_detail12=''#全部商品信息
        goods_detail3={}#部分商品信息，需求字段
        for i in range(3,len(goods_detail1)):
            goods_detail12+=goods_detail1[i].text+','
            goods_detail3[str(goods_detail1[i].text).split('：')[0]]=(goods_detail1[i].text).split('：')[1]
        #print(goods_detail12)
        #print(goods_detail3)
        if '商品毛重' in  goods_detail12:
            good_weight=str(goods_detail3['商品毛重'])
        #print (good_weight)
        else: 
            good_weight='无'
        if '多卡支持' in goods_detail12:
            good_card_support=str(goods_detail3['多卡支持'])
        else:
            good_card_support='无'
        if '机身厚度' in goods_detail12:
            good_width=re.findall(r'\d+',str(goods_detail3['机身厚度']))[0]
        else: 
            good_width='无'
        #print(good_width)
        if '电池容量' in goods_detail12:
            power_size=str(goods_detail3['电池容量'])
        else: 
            power_size='无'
        if '后置摄像头像素' in goods_detail12:
            back_Camera=str(goods_detail3['后置摄像头像素'])
        else: 
            back_Camera='无'
        if '前置摄像头像素' in goods_detail12:
            forward_Camera=str(goods_detail3['前置摄像头像素'])
        else: 
            forward_Camera='无'  
        if '商品产地' in goods_detail12:
            good_birth=str(goods_detail3['商品产地'])
        else: 
            good_birth='无'
        if '机身颜色' in goods_detail12:
            body_color=str(goods_detail3['机身颜色'])
        else: 
            body_color='无'
        if '系统' in goods_detail12:
            moblie_system=str(goods_detail3['系统'])
        else: 
            moblie_system='无'
        if '网络制式' in goods_detail12:
            network_standard=str(goods_detail3['网络制式'])
        else: 
            network_standard='无'
        if '4G LTE网络特性' in goods_detail12:
            G4_network_standard=str(goods_detail3['4G LTE网络特性'])
        else: 
            G4_network_standard='无'
        if '拍照特点' in goods_detail12:
            photo_feature=str(goods_detail3['拍照特点'])
        else: 
            photo_feature='无'
        if '机身内存' in goods_detail12:
            mobile_memory=str(goods_detail3['机身内存'])
        else: 
            mobile_memory='无'
        if '运行内存' in goods_detail12:
            run_memory=str(goods_detail3['运行内存'])
        else: 
            run_memory='无'
        Taidi_goods_Detail={'id':id,'goods_href':goods_href,'good_name':good_name,'mobile_name':mobile_name,'phone_shop':phone_shop,'attraction_title':attraction_title,'previous_price':previous_price,'comment_sum':comment_sum,'paras':paras,'goods_detail12':goods_detail12,'good_weight':good_weight,'good_card_support':good_card_support,'good_width':good_width,'power_size':power_size,'back_Camera':back_Camera,'forward_Camera':forward_Camera,'good_birth':good_birth,'body_color':body_color,'moblie_system':moblie_system,'network_standard':network_standard,'G4_network_standard':G4_network_standard,'photo_feature':photo_feature,'mobile_memory':mobile_memory,'run_memory':run_memory}       
        print('商品详细信息为：'+str(Taidi_goods_Detail))
        collection.insert(Taidi_goods_Detail)
    #html2=requests.post(url_comment,cookies=_cookies,headers=headers,verify=False);#爬取评论信息
    #print(html2.text)
#     comment_data=json.load(html2)#评论数据
#     print(comment_data)
# 
def crawl_good_comments(id,collection):
    n=0
    for i in id:
        
        #n+=1
        #print('正在爬取第'+str(n)+'个商品评论')
        
        url_comment='http://gzjs.bazhuayu.com/comment/'+str(i)#商品评论链接
        html2=requests.post(url_comment,headers=headers,verify=False).text#爬取评论信息
        jsondata=json.loads(html2)#json格式数据
        #print(jsondata)
        if jsondata !=None:        
            for j in jsondata:
                if j ==None:#当j不为空
                    break
                else:
                    comment=j['content']#评论内容
                    score=j['score']#分数
                    goods_comments={'id':str(i),'comment':comment,'score':score}
                    collection.insert(goods_comments)
                    #print(str(goods_comments))
                
            
    
                
if __name__ == '__main__':
    mongo_con=MongoClient('localhost', 27017)
    db=mongo_con.Taidi
    collection=db.goods_comments#商品详细信息
#     for i in range(1,90):   
#         crawl_good_detail(i,collection)            
#     db.close()            
    goods_Detail=pd.read_csv('./goods_Detail.csv')
    name=['华为','苹果','小米']
    goods_Detail_1=goods_Detail[goods_Detail['手机品牌']=='华为']#筛选出包含华为，小米，苹果的数据
    goods_Detail_2=goods_Detail[goods_Detail['手机品牌']=='小米']#筛选出包含华为，小米，苹果的数据
    goods_Detail_3=goods_Detail[goods_Detail['手机品牌']=='苹果']#筛选出包含华为，小米，苹果的数据
    #print(goods_Detail_1.head(100))#
    goods_Detail_1=goods_Detail_1.append(goods_Detail_2)
    goods_Detail_1=goods_Detail_1.append(goods_Detail_3)
    print(goods_Detail_1)
    id=goods_Detail_1columns=['id','手机品牌']
    crawl_good_comments(id,collection)
    db.close()
        
        
    
    
    
