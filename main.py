import requests
import urllib
import time
import json


BVList=['BV1CA411q7ZB', 'BV1of4y1S7Zo', 'BV1nZ4y1K75U', 'BV1gb4y12733', 'BV1N34y1D7QP', 'BV1g34y1d7tf', 'BV17R4y1J7VG', 'BV1QJ41187x8', 'BV1C4411V7yw', 'BV1y4411V7gF', 'BV1Bt4y1r7P6', 'BV12b411v71w', 'BV1fs411y7gT', 'BV1Xt411Z7vo', 'BV1Ma4y1a7XV', 'BV19i4y1A72A', 'BV1pf4y1e7xW', 'BV11K411c7z3', 'BV1JX4y1G7v4', 'BV1F64y1z7q3', 'BV1PA41187qk', 'BV14b411b7xY', 'BV1Gt41137cC', 'BV1tt411U7E8', 'BV1i4411i7km', 'BV1u54y1q777', 'BV1gW411m7Vg', 'BV1R441197Ze', 'BV1GW41127S8', 'BV1MK4y1P7MC', 'BV1nW411U7Qi', 'BV1Dt4y1U7du', 'BV12V411i7Be', 'BV13p411R7Fc', 'BV1tb411A7G9', 'BV1os411f7Hk', 'BV1CJ411D7dC', 'BV1Rt411q7SA', 'BV1oK4y1h7LX', 'BV1HW411X76Y', 'BV1pb411B7GZ', 'BV1Px411E7Fh', 'BV1nX4y1V7Kn', 'BV1EJ411G7bS', 'BV1zJ411J7Ux', 'BV1ep4y197qK', 'BV1n4411q7cf', 'BV1Ws411n7r4', 'BV1gx411m7GA', 'BV1EK411p7YS', 'BV1j7411N7VF', 'BV19v411q7QT', 'BV1UE411e7MP', 'BV1Mt411k7Tz']

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
        title=data['title']
        cid=data['pages'][p-1]['cid']
        return str(cid),title
    else:
        return False,False

def getInformation(bvList):
    infoList=[]
    for bvid in bvList:
        item=[]
        if len(bvid) < 12:
            print("BVID 格式错误")
            continue
        elif len(bvid) == 12:
            cid,title=getCidAndTitle(bvid)
            if(cid == False):
                continue
            item.append(bvid)
        else:
            cid,title=getCidAndTitle(bvid[:12],int(bvid[13:]))
            if(cid == False):
                continue
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
        if "/" in title:
            title = " ".join(title.split("/"))
        if '\\' in title:
            title = " ".join(title.split("\\")) 
        urllib.request.urlretrieve(url=audioUrl, filename='download/'+title+'.mp3')
        ed=time.time()
        print(str(round(ed-st,2))+' seconds download finish:',title)
        time.sleep(1)

if __name__ == '__main__':
    print('Downloader Start!')
    st=time.time()
    getAudio(getInformation(BVList))
    ed=time.time()
    print('Download Finish All! Time consuming:',str(round(ed-st,2))+' seconds')
