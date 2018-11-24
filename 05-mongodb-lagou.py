# -*- coding:utf-8 -*-

import sys, os
import time
import uuid
from pymongo import MongoClient
from fake_useragent import UserAgent

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
    'kd': 'Java',  # Keyword
}

response = requests.post(url, headers=headers, data=payload)


# my_set.insert_one(response.json()['content']['positionResult'])

# Task 3: Pull all data and save into mongodb

def get_uuid():
    return str(uuid.uuid4())


i = 1
remain = True

while remain:

    # Tips: Using fake_agent would help to avoid "您操作太频繁,请稍后再访问"
    # Tips: Using same url too many times, you might hit: 
    # requests.exceptions.SSLError: HTTPSConnectionPool(host='www.lagou.com', port=443): Max retries exceeded with url: /jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1045)')))
    # Even using cookie + fake_agent, if no time.sleep(5), you still will hit "您操作太频繁,请稍后再访问"
    # Actually, I hit it at page 29. Without cookie but only fake_useragent, I hit it at page 5.
    time.sleep(5)
    ua = UserAgent()
    headers['User-Agent'] = ua.random

    cookie = "JSESSIONID=" + get_uuid() + ";" \
            "user_trace_token=" + get_uuid() + "; LGUID=" + get_uuid() + ";" \
            "SEARCH_ID=" + get_uuid() + '; _gid=GA1.2.717841549.1514043316; ' \
            '_ga=GA1.2.952298646.1514043316; ' \
            'LGSID=' + get_uuid() + "; " \
            "LGRID=" + get_uuid() + "; "

    headers['cookie'] = cookie
    print('UA:' + str(headers['User-Agent']))
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200 or not response.json()['success']:
        print(response.json())
        print("Something went wrong!")
        break
    print("Total: " + str(response.json()['content']['positionResult']['totalCount']))
    print("Left: " + str(response.json()['content']['positionResult']['totalCount'] - i * 15))
    print("============================== This is page: [" + str(i) + "] ============================== ")
    print("============================== This is page: [" + str(i) + "] ============================== ")
    print("============================== This is page: [" + str(i) + "] ============================== ")
    # print(response.json())
    count_results = len(response.json()['content']['positionResult']['result'])
    # If we have results, save it
    if count_results > 0:
        my_set.insert_one(response.json()['content']['positionResult'])

    # If still have pages.
    if response.json()['content']['positionResult']['totalCount'] - i * 15 > 0:
        i = i + 1
        payload = {
            'first': 'true',
            'pn': i,
            # This is the page number, you can get totalCount from json, then calculate how much page it would be
            'kd': 'Java',  # Keyword
        }
    else:
        remain = False
