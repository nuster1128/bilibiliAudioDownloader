from urllib import error
import requests
import urllib
import time
import sys
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

def getCidAndTitle(bvid,p=1):
    url='https://api.bilibili.com/x/web-interface/view?bvid='+bvid
    data = getData(url)
    if data != False:
        p_len = len(data['pages'])
        cids = []
        titles = []
        for p in range(p_len):
            # title=data['title']+str(p)
            cids.append(str(data['pages'][p]['cid']))
            titles.append(data['pages'][p]["part"])
        return cids,titles,data["title"]
    else:
        return False,False

def getInformation(bvList):
    infoList=[]
    for bvid in bvList:
        if len(bvid) < 12:
            print("BVID 格式错误")
            continue
        elif len(bvid) == 12:
            cids,titles,folder=getCidAndTitle(bvid)
            if(cids == False):
                continue
            for i in range(len(cids)):
                item=[]
                item.append(bvid)
                item.append(cids[i])
                item.append(titles[i])
                item.append(folder)
                infoList.append(item)

        else:
            cids,titles,folder=getCidAndTitle(bvid[:12],int(bvid[13:]))
            if(cid == False):
                continue
            for i in range(len(cids)):
                item=[]
                item.append(bvid)
                item.append(cids[i])
                item.append(titles[i])
                item.append(folder)
                infoList.append(item)
            

        

    return infoList

def getAudio(infoList):
    baseUrl='http://api.bilibili.com/x/player/playurl?fnval=16&'

    pre_folder = "";
    for item in infoList:
        st=time.time()
        bvid,cid,title=item[0],item[1],item[2]
        url=baseUrl+'bvid='+bvid+'&cid='+cid
        folder = "./download/"+item[3]
        if(not os.path.exists(folder)):
            
            os.makedirs(folder)
            pre_folder = folder
        if(os.path.exists(folder) and folder != pre_folder):
            print(f"与文件夹:./download/{folder}冲突，已经自动跳过该音频或音频合集({bvid})的下载请重命名冲突文件夹的名字")
            continue
        audioUrl=requests.get(url).json()['data']['dash']['audio'][0]['baseUrl']

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            ('Referer', 'https://api.bilibili.com/x/web-interface/view?bvid='+bvid),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        if "/" in title:
            title = " ".join(title.split("/"))
        if '\\' in title:
            title = " ".join(title.split("\\")) 
        try:

            urllib.request.urlretrieve(url=audioUrl, filename=folder+'/'+title+'.mp3')
        except (HTTPError, URLError, ContentTooShortError) as e:
            print("下载失败，因为：", e)
        ed=time.time()
        print(str(round(ed-st,2))+' seconds download finish:',title)
        time.sleep(1)

if __name__ == '__main__':
    BVList = sys.argv[1:]
    print(BVList)
    
    print(f'Downloader Start! {BVList}')
    st=time.time()
    getAudio(getInformation(BVList))
    ed=time.time()
    print('Download Finish All! Time consuming:',str(round(ed-st,2))+' seconds')
