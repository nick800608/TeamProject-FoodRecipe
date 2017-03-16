# coding: utf-8

import requests as r
from bs4 import BeautifulSoup as bs
import json
import csv
from pymongo import *
import re
import sys

url_base = 'http://www.ipeen.com.tw'

def page_crawler():
    try:
        url = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
        res = r.get(url)
        res.encoding="utf-8"
        soup = bs(res.text, 'lxml')
        #取得最後一頁的頁數
        finalpage = soup.select('.next_p_s > a')[0].get('href').split('=')[1]
        int_page = int(finalpage)
        for i in range(1,int_page+1):
            page_url = url+'?p={}'.format(i)
            
            sys.stdout.write(page_url)
            #呼叫取得餐廳裡的所有評論網址的方法
            all_restaurant_list(page_url)
    except IndexError:
        sys.stdout.write("[ERROR] : index error!")
		
def all_restaurant_list(page_url):
    res = r.get(page_url)
    res.encoding="utf-8"
    soup = bs(res.text, 'lxml')
    
    last_list = soup.select('.serShop')[-1].select('h3')[0].get('id').split('_')[2]
    int_list = int(last_list)
    
    for i in range(1,int_list+1):
        try:
            #取到的是/shop/數字
            restaurant_num = soup.select('#shop_h3_{} > a'.format(i))[0].get('href').split('-')[0]
            
#             print(restaurant_num)
            
            #取得每間餐廳評論的最大數目
            restaurant_url = 'http://www.ipeen.com.tw/shop/{}/comments?p=1&sortway=d&so=shop_default'.format(restaurant_num.split('/')[2])
            res_r = r.get(restaurant_url)
            res_r.encoding="utf-8"
            soup_r = bs(res_r.text, 'lxml')
            gray_text = soup_r.select('.info > h1 > span')[0].text
            if "已歇業"not in gray_text:
                total_share = soup_r.select('h2.main-title')[0].text.split('(')[1].split(')')[0]
                int_share = int(total_share)
                int_page=0
                if int_share%5==0:
                    int_page=int(int_share/5)
                else:
                    int_page=int(int_share/5)+1
                for i in range(1,int_page+1):

                    share_page = '/comments?p={}&sortway=d&so=shop_default'.format(i)
                    share_url = url_base + restaurant_num + share_page
                    sys.stdout.write(share_url)
                    restaurant_share(share_url)
        except IndexError:
            sys.stdout.write("[ERROR] : no page!")
			
#爬取單一餐廳的所有食記網址
def restaurant_share(share_url):
    res = r.get(share_url)
    res.encoding="utf-8"
    soup = bs(res.text, 'lxml')

    comment_list = soup.find_all('a',{'itemprop':'discussionUrl url'})
    for comment in comment_list:
        comment_url = comment.get('href')
        c_url = url_base + comment_url
        sys.stdout.write(c_url + '\n')
        comment_crawler(c_url)
		
#爬取食記裡所需要的資料
def comment_crawler(c_url):
    
    try: 
        res = r.get(c_url)
        res.encoding="utf-8"
        soup = bs(res.text, 'lxml')
        mydict = """"""
        
        #作者id
        author_id = soup.find_all('a',{'data-action':'header_user'})[0].get('href').split('../')[1].split('/')[1]
        mydict += author_id
        mydict += '\t'
                
        #發表日期
        created_date = soup.select('.date > span')[0].text.split()[0]
        mydict += created_date
        mydict += '\t'
        
        #種類
        category = soup.find_all('span',{'itemprop':'title'})[4].text
        mydict += category
        mydict += '\t'
        
        #餐廳名稱
        restaurant_name = soup.select('.brief > p > a')[0].text.strip()
        mydict += restaurant_name
        mydict += '\t'
        
        #平均消費
        avg_consume = soup.select('.other > ul > li')[3].text.split('：')[1].strip().split(' ')[0]
        mydict += avg_consume
        mydict += '\t'
        
        #瀏覽人數
        read = soup.select('div.actions > span')[1].text.split(' ')[1]
        if ',' in read:
            r1 = read.split(',')
            r2 = ''.join(r1)
            mydict += r2
            mydict += '\t'
        else:
            mydict += read
            mydict += '\t'
        
        #分享
        share = soup.find('a',{'data-action':'right_shopcomment'}).text.split('人')[0]
        mydict += share
        mydict += '\t'
        
        #美味度
        delicious = soup.select('.rating > dd')[0].text
        mydict += delicious
        mydict += '\t'
        
        #環境氣氛
        dining_environment = soup.select('.rating > dd')[2].text
        mydict += dining_environment
        mydict += '\t'
        
        #服務品質
        service_quality = soup.select('.rating > dd')[1].text
        mydict += service_quality
        mydict += '\t'
        
        #評分
        rate = soup.find('meter',{'max':'50'}).select('span')[0].text
        mydict += rate
        
        #寫進mongoDB
        #goto_mongo(mydict)
        
        #print(mydict)

        #寫進txt檔
        with open('ipeen.txt', 'a',encoding='utf8') as f:
            f.write(mydict)
            f.write('\n')
    except IndexError: 
        sys.stdout.write("[ERROR] : empty comment!" + '\n')
#	except:
#		sys.stdout.write("[ERROR] : ***Issues to be solved***" + '\n')
page_crawler()