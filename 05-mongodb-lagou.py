# -*- coding:utf-8 -*-

import sys, os
from pymongo import MongoClient

# Task 1: Setup Mongo connection
client = MongoClient()
db = client.lagou
my_set = db.set

import requests

# Task 2: Get first page of data from lagou.com
# Direct using below url in browser will see:
# {
#   "success": false,
#   "msg": "您操作太频繁,请稍后再访问",
#   "clientIp": "71.198.44.51"
# }
# Later I figured out that it requires headers with User-Agent and Referer
url = "https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false"

# Please note, there's parameter in Referer you might want to customize.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_Python?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
}

payload = {
    'first': 'true',
    'pn': '1',  # This is the page number, you can get totalCount from json, then calculate how much page it would be
    'kd': 'Python',  # Keyword
}

response = requests.post(url, headers=headers, data=payload)

requests.post(url, headers=headers, data=payload)
my_set.insert_one(response.json()['content']['positionResult'])

# Task 3: Pull all data and save into mongodb
