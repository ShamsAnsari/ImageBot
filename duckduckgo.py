import json
import re

import requests


def search(keywords, result_num=0):
    url = 'https://duckduckgo.com/'
    params = {
        'q': keywords,
    }

    res = requests.post(url, data=params)

    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M | re.I)

    if not searchObj:
        return -1

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('kp', '1'),
        ('l', 'us-en'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    requestUrl = url +  "i.js"

    res = requests.get(requestUrl, headers=headers, params=params)
    data = json.loads(res.text)

    if result_num >= len(data['results']):
        result_num = len(data["results"]) - 1

    if len(data["results"]) == 0:
        return None
    return data["results"][result_num]['image']


def printJson(objs):
    for obj in objs:
        print("Width {0}, Height {1}".format(obj["width"], obj["height"]))
        print("Thumbnail {0}".format(obj["thumbnail"]))
        print("Url {0}".format(obj["url"]))
        print("Title {0}".format(obj["title"].encode('utf-8')))
        print("Image {0}".format(obj["image"]))
        print("__________")
