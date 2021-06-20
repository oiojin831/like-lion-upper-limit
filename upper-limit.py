#!/usr/bin/env python
# coding: utf-8

# In[29]:


from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://finance.naver.com/sise/"
soup = BeautifulSoup(urlopen(url), 'html.parser')


# In[106]:


# top 종목을 inspect 해보니 table안에 필요한 데이터가 다있다.
table = soup.find("table", id="siselist_tab_0")

# heading을 포함한 데이터들은 tr에 들어있다.
# 일단 tr을 전부 가져온다.
all_tr = table.find_all("tr")

# 첫번째 tr만 th를 가지고 있다.
# th의 text를 전부 가져와본다.
print("*" * 10, "th text")
th_tags = all_tr[0].find_all("th")
for th in th_tags:
    print(th.text)

# tr들을 확인해보니 padding 이나 divider를 위한 tr이 존재한다.
# 1,7,8,9,13,14는 나중에 제외해야한다.

# td를 가지는 첫 tr을 print해본다
# 빈공간이 많아서 strip를 사용해서 whitespace를 지움
print("*" * 10, "첫번째 td text")
for td in all_tr[2].find_all("td"):
     print(td.text.strip())
    # em이 있는애가 있다.


# td의 text가 대부분 잘오는데 "전일비"데이터가 whitespace랑 같이 온다
# td tag의 자식으로 바로 text가 있는것이 아니라 em과 span을 가지고 있다.
for td in all_tr[2].find_all("td"):
    # 두개의 span 중 두번째(index 1)로 접근을할려고 하니 등락율도 td의 자식으로 span이 있어서
    # 에러가 뜬다.
    # print(td.find_all("span")[1])
    pass

# 그냥 span으로 찾기보다는 index 번호를 받아서 찾아야겠다.
# list의 index를 for loop에서 가져오기 위해서는 enumerate를 사용해야된다.
print("*" * 10, "정리된 첫번째 td text")
for index, td in enumerate(all_tr[2].find_all("td")):
    # index 5가 "전일비" 데이터 이다.
    if index == 5:
        print(td.find_all("span")[1].text.strip())
    else:
        print(td.text.strip())


    
# tr에 있는 th와 td의 정보를 하나씩 가져와 봤으니
# tr을 loop를 돌려서 모든 데이터를 가져와본다
# 1,7,8,9,13,14는 제외시킨다.
print("*" * 10, "모든 데이터")
for index, tr in enumerate(all_tr):
    if index == 1 or index == 7 or index == 8 or index ==  9 or index == 13 or  index ==14:
        pass
    elif index == 0:
        for th in tr.find_all("th"):
            print(th.text)
    else:
        for index, td in enumerate(tr.find_all("td")):
            if index == 5:
                print(td.find_all("span")[1].text.strip())
            else:
                print(td.text.strip())
    
    


# In[119]:


# all_tr의 loop를 한번 돌때마다 dictionary에 한개의 row의 모든 정보를 저장한다.
# 이 dictionary를 전체 데이터를 포괄하는 list에 저장한다.

all_data = []
keys = []
rank = 0
for index, tr in enumerate(all_tr):
    if index == 1 or index == 7 or index == 8 or index ==  9 or index == 13 or  index ==14:
        continue
    elif index == 0:
        for th in tr.find_all("th"):
            keys.append(th.text.strip())
    else:
        row_data = {}
        rank = rank + 1
        for idx, td in enumerate(tr.find_all("td")):
            if idx == 0:
                row_data[keys[idx]] = str(rank)
            elif idx == 5:
                row_data[keys[idx]] = td.find_all("span")[1].text.strip()
            else:
                row_data[keys[idx]] = td.text.strip()
        all_data.append(row_data)

#import json
#print(json.dumps(all_data, indent=2, ensure_ascii=False))

from pandas import Series, DataFrame
data = DataFrame(all_data)
data


# In[ ]:




