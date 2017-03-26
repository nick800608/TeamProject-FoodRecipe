import requests as r
from bs4 import BeautifulSoup as bs
import json 
from queue import Queue
import threading
import re
import time
import random
import os

pageUrl_pattern = '(http(s)?://)(www\.ipeen.com.tw/search/taiwan/000/1-0-0-0/\?p=)(\d+)'
def all_restaurant_list(page_url):
    print(page_url)
    if re.match(pageUrl_pattern, page_url) == None:        
        print('pageURL is not found')
    else:
        try:
            res = r.get(page_url)
        except HTTPError:
            return None
        res.encoding="utf-8"
        soup = bs(res.text, 'lxml')
		
		initialization_count_number = random.randint(1,4)
        count_number = initialization_count_number

        HOST = 'http://www.ipeen.com.tw'
        all_restaurant_in_h3_list = soup.findAll('h3', {'id':re.compile('shop_h3_\d\d?')})
        try: 
            for restaurant in all_restaurant_in_h3_list:
                if not restaurant.span:
                    if count_number%4==1:
                        f1.write(HOST + restaurant.a['href']+'\n')
                    elif count_number%4==2:
                        f2.write(HOST + restaurant.a['href']+'\n')
                    elif count_number%4==3:        
                        f3.write(HOST + restaurant.a['href']+'\n')
                    else:     
                        f4.write(HOST + restaurant.a['href']+'\n')
        except:
            print('[ERROR]IOexception!')
			
class AWSTimeLimitError(Exception):
    def __init__(self,msg):
        self.message=msg
   
    def __str__(self):
        return self.message

def getExecutionTime(startTime):
    if (time.time() - startTime < 600):
        pass
    else:
        raise AWSTimeLimitError('Time is running out')
		
def reduce_AllPagesListSplitBlock_function(q,startTime):
    try:
        rf = open('all_pages_list_block2.txt', 'r',encoding='utf8')
        pages_str = rf.read()
        
    except FileNotFoundError:
        print("'[ERROR]No such file or directory: 'all_pages_list_block2.txt'")
        raise
        
    if (pages_str==''):
        print('no url!')
        rf.close()
        with open('success_all_pages_list_block2.txt', 'w', encoding='utf8') as wsf:
            wsf.write('success')
        os.remove('all_pages_list_block2.txt')
        
    else:
        pages_list = pages_str.split('\n')
        for pages in range(len(pages_list)):
            q.put(pages_list.pop())		
		
if __name__ == '__main__':   
    
    startTime = time.time()  
    
    q = Queue()
    t1 = threading.Thread(target=reduce_AllPagesListSplitBlock_function, args=(q,startTime,))     
    t1.start()
    t1.join()
	
    f1 = open('all_restaurant_list_block1.txt', 'a+',encoding='utf8')
    f2 = open('all_restaurant_list_block2.txt', 'a+',encoding='utf8')
    f3 = open('all_restaurant_list_block3.txt', 'a+',encoding='utf8')
    f4 = open('all_restaurant_list_block4.txt', 'a+',encoding='utf8')
    
    while not q.empty():
        try:
            getExecutionTime(startTime)
            all_restaurant_list(q.get())
        except AWSTimeLimitError:
            with open('all_pages_list_block2.txt', 'w', encoding='utf8') as wf:
                page = q.get()
                wf.write(page + '\n')
    if q.empty():
        with open('success_all_pages_list_block2.txt', 'w', encoding='utf8') as wsf:
            wsf.write('success')
        os.remove('all_pages_list_block2.txt')
		
    f1.close()
    f2.close()
    f3.close()
    f4.close()
	
    endTime = time.time() 
    totalExecutionTime = str(endTime-startTime)
    print('[INFO]good')
    print('[INFO]TotalExecutionTime = ' + totalExecutionTime)