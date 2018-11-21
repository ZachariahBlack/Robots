# -*- coding:utf-8 -*-

import sys, os
import requests
import json
import pandas as pd

from bclibs.split import print_split


# Step 1: Get data with headers
# print_split("Task 1: Get data with headers") <-- Don't print split cause it will mess up the output of json
# Note:
# For below url, we can get data from browser, but can't get from python
# You will get below:
# (python3-robots) :robots brant.chen$ python level01-04-headers.py
# <html>
# <head><title>400 Bad Request</title></head>
# <body bgcolor="white">
# <center><h1>400 Bad Request</h1></center>
# <hr><center>openresty</center>
# </body>
# </html>

url = "https://www.zhihu.com/api/v4/members/chen-zhi-tao-84-12/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20"
response = requests.get(url).text
# print(response) <-- Print here will fail with above error messages

# In order to get data from Python, we need to set
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'
}

# We only need 'data' node
r = requests.get(url, headers=headers)
# r.encoding = r.apparent_encoding doesn't work, r.apparent_encoding is ascii for zhihu...
# we have to set it manually
r.encoding = 'utf-8'
response = r.json()['data']

# Tips: 
# Even the output of requests is json(), you won't get correct format of json if just stop at below line then dump to python -mjson.tool
# (python3-robots) :robots brant.chen$ python level01-04-headers.py  | python -mjson.tool
# Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
#  

# print(response) # <-- This is the line

# You need to use json lib to dump it as below
# print(json.dumps(response))
# Now you could run: python level01-04-headers.py  | python -mjson.tool 

# Step 2: Using pandas to help
df = pd.DataFrame.from_dict(response)
# Tips:
# from_dict should be applied to data structure which can be converted to dict.
# For example, if using requests.get(url, headers=headers).json() instead of requests.get(url, headers=headers).json()['data']
# df = pd.DataFrame.from_dict(response) will fail as below error messages:
# File "python3-robots/lib/python3.7/site-packages/pandas/core/frame.py", line 7405, in extract_index
# ValueError: Mixing dicts with non-Series may lead to ambiguous ordering.
# 
print(df.head())
# I believe we save the file with correct encoding and the original response was also in correct encoding
# TODO: Need to figure out why it's garbage after openning csv in Excel
df.to_csv('level01-04-headers.csv', encoding='utf-8')
