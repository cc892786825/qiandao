"""

霸王茶姬签到、查券  V1.1

食翔狂魔

环境变量:bwcj_token,多号用#隔开

注意:缺什么依赖就安装什么依赖

"""



import hashlib

import json

import random

import time

import requests

import os

from os import environ, path

from concurrent.futures import ThreadPoolExecutor

import random

import math

import uuid

from datetime import datetime

activity_id = '947079313798000641'

cur_path = path.abspath(path.dirname(__file__))

def load_send():

  global send, mg

  if path.exists(cur_path + "/notify.py"):

    try:

      from notify import send

      print("加载通知服务成功！")

    except:

      send = False

      print("加载通知服务失败~")

  else:

    send = False

    print("加载通知服务失败~")



# 通知服务

load_send()

logObj = {}

send_msg = ""

invalidCks = []

activityData = {"activityId":"947079313798000641","appid":"wxafec6f8422cb357b"}

activityData = {

    "activityId": activity_id,

    "storeId": 49006,

    "timestamp": 0,

    "signature": "",

    "appid": "wxafec6f8422cb357b",

    "store_id": 49006

}

def getUid(token):

    if token == None:

        return None

    else:

        res = requests.get('https://webapi2.qmai.cn/web/catering2-apiserver/crm/customer/card/level/benefits?appid=wxafec6f8422cb357b', headers={

          'Qm-From': 'wechat',

          'Qm-User-Token': token,

          'xweb_xhr': '1',

          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309071d) XWEB/8555',

          'Qm-From-Type': 'catering',

          'Content-Type': 'application/json'

        }).json()

        if res["code"] == '0':

            return res["data"]["upgradeInfoResponse"]["customerId"]

        else:

           return None

def getUserInfo(token):

  url = f'https://webapi.qmai.cn/web/catering/crm/personal-info?appid=wxafec6f8422cb357b'

  rsp = requests.get(url,headers={

    'Qm-From': 'wechat',

    'Qm-User-Token': token,

    'xweb_xhr': '1',

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309071d) XWEB/8555',

    'Qm-From-Type': 'catering',

    'Content-Type': 'application/json'

  }).json()

  if(rsp["message"] == "登录超时"):

    logObj[token] = f"token失效,已删除！"

    invalidCks.append(token)

    return False

  phone = rsp['data']['mobilePhone']

  phone = '****'.join([phone[:3],phone[7:]]) + '----bwcj' + str(random.randint(1, 1000))

  return phone



def getList(phone,token):

  url = f'https://webapi.qmai.cn/web/catering/crm/coupon/list'

  rsp = requests.post(url,headers={

    'Qm-From': 'wechat',

    'Qm-User-Token': token,

    'xweb_xhr': '1',

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309071d) XWEB/8555',

    'Qm-From-Type': 'catering',

    'Content-Type': 'application/json'

  },data=json.dumps({"pageNo":1,"pageSize":1000,"useStatus":0,"appid":"wxafec6f8422cb357b"})).json()

  if rsp['status'] == True:

    for item in rsp['data']['data']:

      logObj[phone] += f'<br />\n券名称:{item["title"]},有效时间:{item["expireDesc"]}。'



def getSignature(timestamp, user_id):

    reversed_activity_id = activity_id[::-1]

    store_id = 49006

    

    params = {

        'activityId': activity_id,

        'sellerId': str(store_id),

        'timestamp': timestamp,

        'userId': user_id

    }

    sorted_params = sorted(params.items())

    query_string = '&'.join(f'{key}={value}' for key, value in sorted_params if value is not None)

    query_string += f'&key={reversed_activity_id}'

    

    md5_hash = hashlib.md5(query_string.encode()).hexdigest().upper()

    

    return md5_hash



def signIn(phone,token):

  url = f'https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign'

  timestamp = time.time_ns() // 1000000

  uid = getUid(token)

  activityData["timestamp"] = timestamp

  activityData["signature"] = getSignature(timestamp, uid)

  rsp = requests.post(url,headers={

    'Qm-From': 'wechat',

    'Qm-User-Token': token,

    'xweb_xhr': '1',

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309071d) XWEB/8555',

    'Qm-From-Type': 'catering',

    'Content-Type': 'application/json'

  },data=json.dumps(activityData))

  rsp = rsp.json()

  print(rsp)

  if rsp['status'] == True:

    logObj[phone] = "签到成功！"

  else:

    logObj[phone] = f'{rsp["message"]}'



def task(token):

  phone = getUserInfo(token)

  if phone != False:

    logObj[phone] = ""

    signIn(phone,token)

    getList(phone,token)



if __name__ == '__main__':

  tokens = os.environ["bwcj_token"].split("#")

  with ThreadPoolExecutor(max_workers=3) as executor:

      result = list(executor.map(task, tokens))

  for item in logObj:

    send_msg += f'{item}:<br />\n{logObj[item]}<br />\n<br />\n'

  if len(invalidCks) > 0:

    send_msg += f'失效Token:<br />\n{"#".join(invalidCks)}<br />\n<br />\n'

  print(send_msg)

  send('霸王茶姬签到查券', send_msg)

