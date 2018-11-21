import sys, os
import urllib.request


f = urllib.request.urlopen('http://google.com')
print(f.read(500))
# Usually, no need to use UTF-8 on English page.
# If it's not UTF-8, decode('utf-8') will show you garbage
# You can try baidu.com, after decode('utf-8'), it can display Chinese characters correctly
# TODO: Need to figure out a method to detect encoding dynamically
print("==============================================================")
print(f.read(500).decode('utf-8'))


import requests

# Notes #1: urllib,requests are the libs being used for get content of remote web pages

r = requests.get("http://google.com")
print("==============================================================")
print(r.text) # TODO: Using default encoding, what's the default encoding?
# If it's UTF-8, like baidu.com, above will show garbage for Chinese characters
r.encoding = "utf-8"
print("==============================================================")
print(r.text)