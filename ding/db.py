from Judge import judge_func
import numpy as np
import pandas as pd
import pymongo
import requests
import hmac
import hashlib
import base64
import urllib.parse
import json
import time
from datetime import datetime as dt
import datetime
TABLE = 'helmen'
client = pymongo.MongoClient('localhost')
db = client['test']
table = db['helmen']
previous_RecordID = []
class dingTalk():
    def __init__(self):
        self.access_token = '5bb414bbd12ccb74196b58cb21893c3a36743889dc78e0ef2a6c5d2888a631d9'
    def get_params(self):
        timestamp = str(round(time.time() * 1000))
        secret = 'SEC3cf584e906ff16ca465b26e7324eba304a8f18f9e88171c4e6c4afcb7cb96326'
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign
    def msg(self, markdown_text):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "test",
                "text": markdown_text

            },
            "at": {
                "isAtAll": False
            }
        }
        json_data = json.dumps(data)
        print(json_data)
        timestamp, sign = self.get_params()
        print(timestamp, sign)
        response = requests.post(
            url='https://oapi.dingtalk.com/robot/send?access_token={access_token}&sign={sign}&timestamp={timestamp}'.format(access_token=self.access_token, sign=sign, timestamp=timestamp), data=json_data, headers=headers)
        return response
dingtalk = dingTalk()
while True:
    l = []
    msg = ''
    now = dt.now()
    five_mins_ago = now + datetime.timedelta(minutes=-6)
    query = {"create_time": {"$gt":five_mins_ago, "$lt":now}}
    items = table.find(query)
    
    for item in items:
        item = dict(item)
        if item['RecordID'] not in previous_RecordID:
            l.append(item['RecordID']) 
            values = []
            for key in item.keys():
                if key!='points' and  key!='create_time' and key!='judge_res':
                    values.append(item[key])
            # print(values)        
    
            msg += '\n\n\n---------------------------------------------\n\n\n'
            msg += ' \n\n '.join([str(i) for i in values])
            msg += '\n\n![screenshot](http://58.87.111.39/img/{TABLE}_{RecordID}.png)\n\n\n'.format(TABLE=TABLE, RecordID=item['RecordID'])
            msg += '\n\n\n---------------------------------------------\n\n\n'
            # judge      
            judge_res = '无效' if int(item['judge_res']) == 0 else '有效'
            msg += '判断结果:' + judge_res  
    print('messagea:')
    print(msg)
    response = dingtalk.msg(msg)
    print(response.text)
    print("sleep 5 mins")
    time.sleep(5*60)
     
