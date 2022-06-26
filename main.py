import requests
import urllib
import time
import sys

def getCidAndTitle(bvid,p=1):
    url='https://api.bilibili.com/x/web-interface/view?bvid='+bvid
    data=requests.get(url).json()['data']
    title=data['title']
    cid=data['pages'][p-1]['cid']
    return str(cid),title

def getInformation(bvList):
    infoList=[]
    for bvid in bvList:
        item=[]
        if len(bvid) == 12:
            cid,title=getCidAndTitle(bvid)
            item.append(bvid)
        else:
            cid,title=getCidAndTitle(bvid[:12],int(bvid[13:]))
            item.append(bvid[:12])
        item.append(cid)
        item.append(title)
        infoList.append(item)

    return infoList

def getAudio(infoList):
    baseUrl='http://api.bilibili.com/x/player/playurl?fnval=16&'

    for item in infoList:
        st=time.time()
        bvid,cid,title=item[0],item[1],item[2]
        url=baseUrl+'bvid='+bvid+'&cid='+cid

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
        urllib.request.urlretrieve(url=audioUrl, filename='download/'+title+'.mp3')
        ed=time.time()
        print(str(round(ed-st,2))+' seconds download finish:',title)
        time.sleep(1)

if __name__ == '__main__':
    BVList = sys.argv[1:]
    print(f'Downloader Start! {BVList}')
    st=time.time()
    getAudio(getInformation(BVList))
    ed=time.time()
    print('Download Finish All! Time consuming:',str(round(ed-st,2))+' seconds')
