import argparse
import requests
import time
import json
import os


url = "https://api.bilibili.com/x/v3/fav/resource/list"

# 如果是私密收藏夹，可以直接在浏览器中复制cookies
cookies = open('cookie.txt', 'r').read()

headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-US;q=0.6',
    'cookie': cookies,
    'origin': 'https://space.bilibili.com',
    'referer': 'https://space.bilibili.com',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}


def get_fav_list(fid):
    pn = 1
    ps = 20
    keyword = ""
    order = "mtime"
    tid = "0"
    platform = "web"
    bvids = []
    count = 0

    while True:
        print("Page: " + str(pn))
        params = {
            'media_id': fid,
            'pn': pn,
            'ps': ps,
            'keyword': keyword,
            'order': order,
            'type': '0',
            'tid': tid,
            'platform': platform,
        }
        response = requests.get(url, params=params, headers=headers)
        data = json.loads(response.text).get("data")
        favs = data.get("medias")
        for fav in favs:
            bvids.append(fav.get("bvid"))
            count += 1
            print(str(count) + ": " + fav.get("bvid"))
        if not data.get("has_more"):
            print("no more")
            break
        pn += 1
        time.sleep(1)

    print(bvids)
    flags = os.O_RDWR | os.O_CREAT
    fd = os.open("./bvids.txt", flags)
    for bvid in bvids:
        os.write(fd, (bvid + "\n").encode("utf-8"))
    os.close(fd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="the fid of the fav list")
    args = parser.parse_args()
    fid = args.f
    get_fav_list(fid)


main()