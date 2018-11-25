# -*- coding:utf-8 -*-

import sys,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from pymongo import MongoClient
import re

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)

client = MongoClient()
db = client.taobao
data = db.data

def search(kd):
    try:
        browser.get('https://www.taobao.com/')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mq"))) # 
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_PopSearch > div.sb-search > div > form > input[type="submit"]:nth-child(2)')))
        input.send_keys(kd)
        submit.click()
        print("Before getting page number...")
        total = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        print("After getting page number...[" + str(total) + "]")
        get_products()
        return total.text
    except TimeoutException:
        return 0

def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.iterm.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            # 'title': item.find('.deal-cnt').text()[:-3]
            'title': item.find('.title').text(),
            'shot': item.find('.shop').text(),
            'location': item.find('.location').text(),
        }
        print(product)
        data.insert(product)

def main(kd):
    total = search(kd)
    total = int(re.compile('(\d+)').search(total).group(1))

    # If want to pull all data, replace 10 with total + 1
    for i in range(2, 10):
        next_page(i)


if __name__ == '__main__':
    main('玩具')