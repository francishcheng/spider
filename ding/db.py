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
            # "markdown": markdown,
            "markdown": {
                # "title": "检测结果",
                "title": "test",
                "text": markdown_text

            },
            "at": {
                "isAtAll": False
            }
        }
        json_data = json.dumps(data)
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
    results = table.find(query)
    for result in results:
        if result['RecordID'] not in previous_RecordID:
            print(result['RecordID'])
            l.append(result['RecordID']) 
            msg += result['RecordID'] + ','
    previous_RecordID = l
    dingtalk.msg(msg)
    print("sleep 5 mins")
    time.sleep(5*60)
     