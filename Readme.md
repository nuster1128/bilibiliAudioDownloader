# BilibiliAudioDownloader

原作者现在停止更新，但是由于B站的更新，原作者的代码已经无法使用了，所以我fork了一份，进行了优化更新。

**[Version 3.0]**

本项目已于2024年2月1日优化更新至3.0版本。

更新：

- 提供了无损音频下载
- 提供简介的下载
- 支持从收藏夹获取BV号下载
- 增加转码模块，B站直接下载的MP3文件编码格式不被Apple Music支持，需要额外转码
- 更新了依赖包的版本，并优化了代码结构
- 删除了exe文件，并不再提供exe打包支持

P.S. 感谢各位提PR和共同维护的朋友们！

## 项目目的

很喜欢 Vocaloid，但是大多数中P首发都在B站（原MikuFans），自然而然地，B站收藏夹成了歌单

但是每次想听歌的时候都要打开B站，实在太麻烦了，而且B站缓存也不好用，所以开始维护这个爬虫项目

## 主要功能

输入视频BV号列表或收藏夹ID，批量下载B站视频中的音频到本地。

## 使用方法

下载本代码并安装相应的依赖库。

```shell
git clone https://github.com/love98ooo/bilibiliAudioDownloader.git
cd bilibiliAudioDownloader
pip install -r requirements.txt
```

### 下载音乐

#### 方式1 文件批量下载

新建一个txt文件或csv文件存放要下载的bv号，如 `input.txt` 或 `input.csv`。每行输入一个bv号，如

```
BV1AL4y1L7cg
BV1dZ4y1q7F2
```

运行程序，其中 `filename` 为刚才创建的文件名。

```shell
python run.py -f <filename>
```

比如文件名为，如input.txt，则为

```
python run.py -f input.txt
```

最终音频文件将下载到 `download` 文件夹中。

#### 方式2 命令行批量下载

运行程序，其中 `BV1 BV2 ...` 为需要下载的BV号。

```shell
python run.py -c <BV1> <BV2> ...
```

比如要下载 `BV1AL4y1L7cg` 和 `BV1dZ4y1q7F2` 两个音频，则为

```shell
python run.py -c BV1AL4y1L7cg BV1dZ4y1q7F2
```

#### 方式3 从收藏夹下载

运行以下命令获取收藏夹的BV号，其中 `fav_id` 为收藏夹的id，默认输出文件名为 `bvids.txt`

```shell
python fav_list.py -f <fav_id>
```

运行以下命令下载收藏夹中的音频

```shell
python run.py -f bvids.txt
```

#### 注意事项

保存目录：最终音频文件将保存到 `./download` 目录下

分P视频：如果不是分P的视频，只需要BV号即可，如 `BV1aK4y1a7sd`；如果是视频中的某一P，需要在BV号后用'-'注明是第几P， 如 `BV1aK4y1a7sd-1`

Cookie：下载高品质的音频和查看私密收藏夹需要登录，登录后将cookie保存到`cookie.txt`文件中，程序会自动读取cookie文件中的内容

### MP3转码

B站直接下载的MP3文件编码格式不被Apple Music支持，需要额外转码

```shell
python transcode.py
```

转码完成后，会在`./download`目录下生成`output`文件夹，里面存放转码后的音频文件

## 声明

请尊重原视频的作者的版权，禁止用于任何商业用途！

本项目参考了 https://github.com/SocialSisterYi/bilibili-API-collect 中部分内容，感谢作者及其他贡献者。

