
# coding: utf-8

# In[ ]:





# In[ ]:


import requests
from bs4 import BeautifulSoup
for i in range(40000,40100):
    HOST = 'http://www.dodocook.com/recipe/'
    url=HOST+str(i)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    #title
    mydict={}
    for tag1 in soup.select(".band > h1"):
        title=tag1.text
    mydict["title"]=title
        
    #foodname
    foodName=[]
    for tag2 in soup.select(".body > .list > .name"):
        tag2_dict={}
        n=soup.select(".body > .list > .name").index(tag2)
        tag2_dict[tag2.text]=soup.select(".ingredient > .body > .list > .count")[n].text
        foodName.append(tag2_dict)
    mydict["foodName"]=foodName
    
    #step
    step1=[]
    step_list1=soup.select('.steps > .CSrtB > .Sno') 
    step_go1=soup.select('.steps > .CSrtB > .SBpma')
    for tag in step_go1:
        print()
#     step2=[] 
#     step_list2=soup.select('.steps > .CSrtA > .SrtAk > .Sno') 
#     step_go2=soup.select('.steps > .CSrtA > .SrtAk > .Spma > p')
#     for tag4 in step_go2:
#         print(tag4.text)
        
    
    for tag3 in step_list1:
        tag3_dict={}
        n1=step_list1.index(tag3)
        tag3_dict[tag3.text]=step_go1[n1].text
        step1.append(tag3_dict)
       ( while(len(step1)!=0):
        mydict["step"]=step1  )
        
#     for tag4 in step_list2:
#         tag4_dict={}
#         n2=step_list2.index(tag4)
#         tag4_dict[tag4.text]=step_go2[n2].text
#         step2.append(tag4_dict)
#     mydict["step"]=step2
#    ( if len(step1)==0:
#         print("error")
#     else:
#          print(mydict))
        


# In[ ]:



