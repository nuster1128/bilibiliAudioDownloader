# BilibiliAudioDownloader

## 最后更新时间

Version 1.0	2021.2.22

## 项目目的

一直超爱钢琴曲和小提琴曲，而且喜欢流行音乐的钢琴曲和小提琴曲。

最近在B站发现了好多好棒的UP主发弹奏视频，但是B站视频的播放列表太麻烦，而且貌似不能挑自己喜欢的组成歌单。

想在网易云听但是又没有hhhhh，所以某日张小白反手写了个spider脚本来下载B站视频中的音频，然后建列表导入来听，妙哇。

## 主要功能

输入视频BV号列表，批量下载B站视频中的音频到本地。

## 使用方法

1.下载代码并安装相应依赖库。

2.运行 python main.py BV1AL4y1L7cg BV1dZ4y1q7F2 ...（多个bv号以空格分割）

备注：如果不是多P的视频，只需要BV号即可，如['BV1aK4y1a7sd',...]；如果是视频中的某一P，需要在BV号后用'-'注明是第几P，如['BV1aK4y1a7sd-1']。

3.运行main.py开始运行程序，最终音频文件将下载到download文件夹中。

## Python版本与依赖库

Python 3.7

requests, urllib, time

## 声明

请尊重原视频的作者的版权，禁止用于任何商业用途！

本项目参考了https://github.com/Henryhaohao/Bilibili_video_download和https://github.com/SocialSisterYi/bilibili-API-collect中部分内容，感谢两位作者。

本项目作者联系方式:997577114@qq.com

