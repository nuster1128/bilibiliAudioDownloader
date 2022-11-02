# BilibiliAudioDownloader

**[Version 2.0]**

本项目已于2022年11月2日优化更新至2.0版本。

优化更新特性：

- 更新了Python环境和依赖包的版本，并优化了代码。
- 更新了使用方法，支持文件批量下载、命令行下载。
- 新增了应用程序的使用方法，可直接使用exe文件直接进行下载，不必配置Python环境。

p.s. 感谢各位提PR和共同维护的朋友们！

## 项目目的

一直超爱钢琴曲和小提琴曲，而且喜欢流行音乐的钢琴曲和小提琴曲。

最近在B站发现了好多好棒的UP主发弹奏视频，但是B站视频的播放列表太麻烦，而且貌似不能挑自己喜欢的组成歌单。

想在网易云听但是又没有hhhhh，所以某日张小白反手写了个spider脚本来下载B站视频中的音频，然后建列表导入来听，妙哇。

## 主要功能

输入视频BV号列表，批量下载B站视频中的音频到本地。

## 使用方法

### 方式1 文件批量下载

1. 下载本代码并安装相应的依赖库。

```shell
git clone git@github.com:nuster1128/bilibiliAudioDownloader.git
cd bilibiliAudioDownloader
pip install -r requirements.txt
```

2. 新建一个txt文件或csv文件存放要下载的bv号，如input.txt或input.csv。每行输入一个bv号，如

```
BV1AL4y1L7cg
BV1dZ4y1q7F2
```

可参考代码包里给出的一个input.txt的示例。

3. 运行程序，其中`filename`为刚才创建的文件名。

```shell
python run.py -f filename
```

比如文件名为，如input.txt，则为

```
python run.py -f input.txt
```

4. 最终音频文件将下载到`download`文件夹中。

备注：如果不是多P的视频，只需要BV号即可，如`BV1aK4y1a7sd`；如果是视频中的某一P，需要在BV号后用'-'注明是第几P，`BV1aK4y1a7sd-1`。

### 方式2 命令行批量下载

1. 下载本代码并安装相应的依赖库。

```shell
git clone git@github.com:nuster1128/bilibiliAudioDownloader.git
cd bilibiliAudioDownloader
pip install -r requirements.txt
```

2. 运行程序，其中`BV1 BV2 ...`为需要下载的BV号。

```shell
python run.py -c BV1 BV2 ...
```

比如要下载BV1AL4y1L7cg和BV1dZ4y1q7F2两个音频，则为

```shell
python run.py -c BV1AL4y1L7cg BV1dZ4y1q7F2
```

3. 最终音频文件将下载到`download`文件夹中。

备注：如果不是多P的视频，只需要BV号即可，如`BV1aK4y1a7sd`；如果是视频中的某一P，需要在BV号后用'-'注明是第几P，`BV1aK4y1a7sd-1`。

### 方式3 直接通过exe批量下载

1. 双击run.exe。
2. 修改`input.txt`中的内容，每行为一个BV号。

然后输入以下命令开始下载

```
-f input.txt
```

3. 最终音频文件将下载到`download`文件夹中。

## Python版本与依赖库

```
Python 3.9
requests==2.28.1
```

## 声明

请尊重原视频的作者的版权，禁止用于任何商业用途！

本项目参考了 https://github.com/Henryhaohao/Bilibili_video_download 和 https://github.com/SocialSisterYi/bilibili-API-collect 中部分内容，感谢两位作者。

本项目作者联系方式: wfzhangzeyu@163.com

