from .settings import DB, TABLE
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class PachongPipeline:
    def __init__(self):
        #连接数据库
        self.client = pymongo.MongoClient('localhost')
        #创建库
        self.db = self.client[DB]
        ##创建表
        self.table = self.db[TABLE]

    def process_item(self, item, spider):
        # print(item)
        query = {
           'RecordID' : item['RecordID'] 
        }
        res = self.table.find_one(query)
        if res is None:
            try:
                x = self.table.update_one(query, {'$set':dict(item)}, upsert=True)
        # self.table.insert(dict(item)) 
            except:
                print('e')
                print('error updating db')
        return item

