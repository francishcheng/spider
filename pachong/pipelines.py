from .settings import DB, TABLE, IMG_SAVE_PATH
import time
import requests
import scrapy
import json
import matplotlib.pyplot as plt
from itemadapter import ItemAdapter
import numpy as np
import pandas as pd
import pymongo
from .Judge import judge_func
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

post_img_url = 'http://58.87.111.39:5555/items/'

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
                # judge function
                points = item['points']
                points = [int(i) for i in points.split(',')[:-1]]
                points = np.array(points)
                C_ygz = int(item['CValue'])
                Ce = item['sBatchCode']
                xm = item['sItemName']
                judge_res = judge_func(points, Ce, C_ygz, xm)
                item['judge_res'] = int(judge_res)
                # save data            
                x = self.table.update_one(query, {'$set':dict(item)}, upsert=True)

                # fig, ax = plt.subplots()
                # points = item['points']
                # points = [int(point) for point in points.split(',')[:-1]]
                # ax.plot(range(len(points)), points)                 
                # plt.savefig('{IMG_SAVE_PATH}{TABLE}_{RecordID}.png'.format(IMG_SAVE_PATH=IMG_SAVE_PATH, TABLE=TABLE, RecordID=item['RecordID']))

                data = {
                    "points":item["points"], 
                    "TABLE":  TABLE,
                    "RecordID": item["RecordID"]
                }
                headers = {
                    'Connection': 'close',
                }
                json_data = json.dumps(data)
                response = requests.post(post_img_url, headers=headers, data=json_data)
                if response.status_code != 200:
                    print("cannot upload img"+ str(item['RecordID'])) 
            except Exception as e:
                print(e)
                print('error updating db')
        return item

