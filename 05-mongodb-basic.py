# -*- coding:utf-8 -*-

import sys, os
from pymongo import MongoClient

client = MongoClient()
db = client.test
my_set = db.set
my_set.insert_one({"name":"test01",})
