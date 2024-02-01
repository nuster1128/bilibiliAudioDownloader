from urllib.error import HTTPError, URLError, ContentTooShortError
from enum import Enum
import requests
import urllib
import time
import argparse
import csv
import re


class Quantity(Enum):
    MP3 = "mp3"
    FLAC = "flac"


cookies = open('cookie.txt', 'r').read()


headers = {
    'authority': 'api.bilibili.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': cookies,
    'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
}


def get_basic_info(bvid, p=1):
    url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid
    resp = requests.get(url, headers=headers)
    if resp.status_code >= 300:
        print("HTTP ERROR:", resp.status_code)
        raise HTTPError
    json_data = resp.json()
    if "data" not in json_data:
        print("找不到数据")
        raise KeyError
    data = resp.json()['data']
    title = data['title']
    cid = data['pages'][p - 1]['cid']
    pic = data['pic']
    description = data['desc']
    item = [bvid, cid, title, pic, description]
    return item


def get_information(bv_list):
    info_list = []
    for bvid in bv_list:
        if len(bvid) < 12:
            print("bvid 格式错误")
            continue
        elif len(bvid) == 12:
            item = get_basic_info(bvid)
        else:
            item = get_basic_info(bvid[:12], int(bvid[13:]))
        if not item[1]:
            continue
        info_list.append(item)
    return info_list


def get_audio_and_pic(info_list):
    base_url = 'https://api.bilibili.com/x/player/playurl'

    for item in info_list:
        start_time = time.time()
        bvid, cid, title, description = item[0], item[1], item[2], item[4]
        print(f'开始下载 {title} 的音频和封面')
        params = {
            'fnval': '16',
            'bvid': bvid,
            'cid': cid,
        }
        response = requests.get(base_url, headers=headers, params=params).json()['data']['dash']
        if response['flac'] is not None and response['flac']['audio'] is not None:
            audio_url = response['flac']['audio']['base_url']
            qn = Quantity.FLAC
        else:
            audio_url = response['audio'][0]['base_url']
            qn = Quantity.MP3
        print(f'音频格式：{qn.name}')

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            ('Referer', 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
            ('Cookie', cookies)
        ]
        urllib.request.install_opener(opener)
        if "/" in title:
            title = " ".join(title.split("/"))
        if '\\' in title:
            title = " ".join(title.split("\\"))
        title = re.sub(r'[\\/:*?"<>|]', " ", title)
        try:
            urllib.request.urlretrieve(url=audio_url, filename='download/' + title + '.' + qn.value)
            urllib.request.urlretrieve(url=item[3], filename='download/' + title + '.jpg')
            f = open('download/' + title + ".txt", "w", encoding="utf-8")
            f.write(description)
            f.close()
        except (HTTPError, URLError, ContentTooShortError, OSError) as e:
            print(f"下载 {bvid} 失败，因为：{e}")
        end_time = time.time()
        print(f'Download finished in {str(round(end_time - start_time, 2))} seconds!\n')
        time.sleep(1)


def get_bv_list(arg, extra_args):
    bv_list = []
    if arg.f:
        with open(extra_args[0], 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                bv_list.append(line[0])
    elif arg.c:
        bv_list = [i for i in extra_args]

    else:
        raise 'Please select an input method.'

    return bv_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store_true')
    parser.add_argument('-c', action='store_true')
    args, extra_args = parser.parse_known_args()
    bv_list = get_bv_list(args, extra_args)

    print(f'Downloader Start! {bv_list}')
    st = time.time()
    get_audio_and_pic(get_information(bv_list))
    ed = time.time()
    print('Download Finish All!\nTime consuming:', str(round(ed - st, 2)) + ' seconds')


main()