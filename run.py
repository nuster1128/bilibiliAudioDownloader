from urllib import error
# 发送请求
import requests
# 网页内容抓取分析(发送请求)
import urllib
# 时间相关(程序性能分析)
import time
# 命令行解析
import argparse
# 文件读写
import csv
# 系统相关
import os


def getData(url):
    resp = requests.get(url)
    if resp.status_code >= 300:
        print("HTTP ERROR:", resp.status_code)
        return False
    jsonData = resp.json()
    if "data" not in jsonData:
        print("找不到数据")
        return False
    return resp.json()['data']


def getCidAndTitle(bvid, p=1):
    url = 'https://api.bilibili.com/x/web-interface/view?bvid='+bvid
    data = getData(url)
    if data != False:
        title = data['title']
        cid = data['pages'][p-1]['cid']
        part = data['pages'][p-1]['part']
        page = p
        return str(cid), title, part, page
    else:
        return False, False


def getInformation(bvList):
    infoList = []
    for bvid in bvList:
        item = []
        if len(bvid) < 12:
            print("BVID 格式错误")
            continue
        elif len(bvid) == 12:
            cid, title, part, page = getCidAndTitle(bvid)
            if (cid == False):
                continue
            item.append(bvid)
        else:
            cid, title, part, page = getCidAndTitle(bvid[:12], int(bvid[13:]))
            if (cid == False):
                continue
            item.append(bvid[:12])
        item.append(cid)
        item.append(title)
        item.append(part)
        item.append(page)
        infoList.append(item)

    return infoList


def getAudio(infoList):
    baseUrl = 'http://api.bilibili.com/x/player/playurl?fnval=16&'

    for item in infoList:
        st = time.time()
        bvid, cid, title, part, page = item[0], item[1], item[2], item[3], item[4]
        url = baseUrl+'bvid='+bvid+'&cid='+cid

        audioUrl = requests.get(url).json(
        )['data']['dash']['audio'][0]['baseUrl']

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            # 注意修改referer,必须要加的!
            ('Referer', 'https://api.bilibili.com/x/web-interface/view?bvid='+bvid),
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        if "/" in title:
            title = "-".join(title.split("/"))
        if '\\' in title:
            title = " ".join(title.split("\\"))
        if '?' in title:
            title = "？".join(title.split("?"))
        if ':' in title:
            title = "：".join(title.split(":"))
        if '*' in title:
            title = " ".join(title.split("*"))
        if '"' in title:
            title = "“".join(title.split("\""))
        if '<' in title:
            title = " ".join(title.split("<"))
        if '>' in title:
            title = " ".join(title.split(">"))
        if '|' in title:
            title = " ".join(title.split("|"))
        if (part == title):
            print('Downloading ' + str(page) + '.' + title + '.mp3')
            try:
                urllib.request.urlretrieve(url=audioUrl, filename='download/' + str(page) + '.' + title + '.mp3')
            except (error.HTTPError, error.URLError, error.ContentTooShortError) as e:
                print("下载失败，因为：", e)
        else:
            print('Downloading: ' + title + ' ' + str(page) + '.' + part + '.mp3')
            try:
                os.makedirs('./download/' + title, exist_ok=True)
                if "/" in part:
                    part = "-".join(part.split("/"))
                if '\\' in part:
                    part = " ".join(part.split("\\"))
                if '?' in part:
                    part = "？".join(part.split("?"))
                if ':' in part:
                    part = "：".join(part.split(":"))
                if '*' in part:
                    part = " ".join(part.split("*"))
                if '"' in part:
                    part = "“".join(part.split("\""))
                if '<' in part:
                    part = " ".join(part.split("<"))
                if '>' in part:
                    part = " ".join(part.split(">"))
                if '|' in part:
                    part = " ".join(part.split("|"))
                urllib.request.urlretrieve(url=audioUrl, filename='download/' + title + '/' + str(page) + '.' + part + '.mp3')
            except (error.HTTPError, error.URLError, error.ContentTooShortError) as e:
                print("下载失败，因为：", e)
        ed = time.time()
        if (part == title):
            print(str(round(ed-st, 2))+' seconds download finish: ' + str(page) + '.', title + '.mp3')
        else:
            print(str(round(ed-st, 2))+' seconds download finish: ' + title + ' ' + str(page) + '.', part + '.mp3')
        time.sleep(1)


def getBVList(arg, extra_args):
    BVList = []
    if arg.f:
        with open(extra_args[0], 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                BVList.append(line[0])
    elif arg.c:
        BVList = [i for i in extra_args]

    else:
        raise 'Please select an input method.'

    return BVList


# 检测脚本在命令行运行
if __name__ == '__main__':
    os.makedirs('./download', exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store_true')
    parser.add_argument('-c', action='store_true')
    args, extra_args = parser.parse_known_args()
    BVList = getBVList(args, extra_args)

    print(f'Downloader Start! {BVList}')
    st = time.time()
    getAudio(getInformation(BVList))
    ed = time.time()
    print('Download Finish All! Time consuming:',str(round(ed-st, 2))+' seconds')
