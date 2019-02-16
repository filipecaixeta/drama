# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy import DropItem

class MyasiantvPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
        	'mongodb://mexicano:delicia69@ds131729.mlab.com:31729/draminha'
        )
        self.db = connection['draminha']
        #self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
    	self.db['tabela'] =
        return item