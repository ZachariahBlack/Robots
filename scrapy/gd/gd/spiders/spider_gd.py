# -*- coding: utf-8 -*-
import scrapy
from pyquery import *


class SpiderGdSpider(scrapy.Spider):
    name = 'spider_gd'
    allowed_domains = ['glassdoor.com']
    start_urls = ['https://www.glassdoor.com/Job/']

    def parse(self, response):
        
        jpy = PyQuery(response.text)
        li_text = jpy('div.prefooter-module-col:nth-child(2) > ul:nth-child(2) > li').items()
        # Output:
        # text:Dermatologist Jobs
        # text:Administrative Assistant Jobs
        # text:Clerical Jobs
        # text:Receptionist Jobs
        # text:Project Manager Jobs
        # text:More
        for item in li_text:
            print('text:' + item.text())

        

