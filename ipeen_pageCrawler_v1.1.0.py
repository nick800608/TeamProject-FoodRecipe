import requests as r
from bs4 import BeautifulSoup as bs
import json 
from queue import Queue
import threading
import re
import time
url_base = 'http://www.ipeen.com.tw'

def page_crawler():
    startTime = time.time()
    try:
        url = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
        res = r.get(url)
        res.encoding="utf-8"
        soup = bs(res.text, 'lxml')
        page_url_list=[]
        finalpage = soup.select('.next_p_s > a')[0].get('href').split('=')[1]
        int_page = int(finalpage)
        
        f1 = open('all_pages_list_block1.txt', 'a',encoding='utf8')
        f2 = open('all_pages_list_block2.txt', 'a',encoding='utf8')
        f3 = open('all_pages_list_block3.txt', 'a',encoding='utf8')
        f4 = open('all_pages_list_block4.txt', 'a',encoding='utf8')
        
        try:
            for page_number in range(1,int_page+1):
                page_url = url+'?p={}'.format(page_number)

                #print(page_url)
                if page_number%4==1:
                    f1.write(page_url+'\n')

                elif page_number%4==2:
                    f2.write(page_url+'\n')
                elif page_number%4==3:        
                    f3.write(page_url+'\n')
                else:     
                    f4.write(page_url+'\n')
        except:
            pass
            print('[ERROR]IOexception!')
        finally:
            f1.close()
            f2.close()
            f3.close()
            f4.close()
        endTime = time.time()
        print(endTime-startTime)
    except IndexError:
        print("[ERROR] : index error!")
