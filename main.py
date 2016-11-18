# coding: utf-8
import os
import requests
import json
import math
from datetime import datetime,  timedelta

def get_events(period):
    baseurl = "https://ctftime.org/api/v1/events/?limit=100"
    start = datetime.now()
    fin = start + timedelta(days=period)
    print fin
    range_param = "&start={start}&finish={fin}".format(start=start.strftime('%s'), fin=fin.strftime('%s') )
    response = requests.get(baseurl + range_param)
    res = json.loads(response.text)
    return res

def away_from(start):
    now = datetime.now()
    return start - now  #現在時間との差分を返す


def create_message(infos):
    message = ""
    for info in infos:
        if not info['onsite']: #onsite形式のみ表示
            start = datetime.strptime(info['start'],'%Y-%m-%dT%H:%M:%S+00:00') + timedelta(hours=9)#時差合わせして
            d = away_from(start)
            delta_hours =  int(d.total_seconds()/(60*60))
            if delta_hours > 48:#48時間以上後のイベントは表示させない
                return message
            message += info['title'] + u"まで"
            message += u"あと約{hour}時間({start})\n".format(hour=delta_hours, start=start)
            message += info['ctftime_url'] + u"\n"
    return message

def send2slack(text):
    url = os.getenv('SLACK_WEBHOOK_URL')#環境変数にWebhookのURLを入れておく
    payload = {'text': text, 'username': "ctftime-bot", "icon_emoji": ":robot_face:"}
    res = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json', 'charset':'utf-8'})
    print res.content

infos =  get_events(7) #1週間分取得
message = create_message(infos)
send2slack(message)
