import sys, os
import requests
from lxml import etree

from bclibs.split import print_split


url = "https://book.douban.com/subject/3633461/comments/"

r = requests.get(url).text
s = etree.HTML(r)
# Task 1: Get individual item by copying xpath from browsers
print_split("Task 1: Get individual item by copying xpath from browsers")
print(s.xpath('//*[@id="comments"]/ul[1]/li[1]/div[2]/p/span/text()'))

# Task 2: Write xpath other than copying from browsers
# Tips: Once identify the class, you need to still keep the sub level structure
#       As below, we need to specify /p/span, because the content is in <span>
#       You can't just //div[@class="comment"]/p/text()
print_split("Task 2: Write xpath other than copying from browsers")
print("\n\n".join(s.xpath('//div[@class="comment"]/p/span/text()')))

# Task 3: Get all urls in whole file
print_split("Task 3: Get all urls in whole file")
for link in s.iterfind('.//a[@href]'):
    print(link.get('href'))

# Task 4: Get specific scope links
print_split("Task 4: Get specific scope links")
nav_links = s.xpath('//div[@class="nav-items"]/ul/li/a[@href]')
for link in nav_links:
    print(link.text + ": " + link.get('href'))



