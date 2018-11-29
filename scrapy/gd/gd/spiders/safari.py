# -*- coding: utf-8 -*-
import scrapy
from pyquery import *
import json


class SafariSpider(scrapy.Spider):
    name = 'safari'
    allowed_domains = ['oreilly.com']
    # Get TOC of Book: Advanced Linux System Administration
    start_urls = ['https://www.oreilly.com/library/view/advanced-linux-system/9781789132748/']

    def parse(self, response):
        jpy = PyQuery(response.text)
        chapters = jpy('.toc-level-1').items()
        
        for chapter in chapters:
            chapter_title = chapter('a:first').text()

            sub_chapters_titles = []
            for sub_chapter in chapter('.toc-level-2 > a'):
                sub_chapters_titles.append(sub_chapter.text)
            yield {chapter_title:sub_chapters_titles}