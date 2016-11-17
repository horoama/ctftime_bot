# coding: utf-8
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
        if not info['onsite']:
            start = datetime.strptime(info['start'],'%Y-%m-%dT%H:%M:%S+00:00') + timedelta(hours=9)#時差合わせして
            d = away_from(start)
            delta_hours =  int(d.total_seconds()/(60*60))
            if delta_hours > 48:
                return message
            message += info['title'] + u"まで"
            message += u"あと約{hour}時間({start})\n".format(hour=delta_hours, start=start)
            message += info['ctftime_url'] + u"\n"
    return message

infos =  get_events(7)

print create_message(infos)
