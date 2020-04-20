# /usr/bin/env python
# -*- coding:utf-8 -*-
# author: Handsome Lu  time:2020/4/19

from moviepy.editor import *
from moviepy.audio.fx import all
from moviepy.video.tools.subtitles import SubtitlesClip
import os
import eyed3
import random
from aip import AipSpeech
import easygui as g
import sys
import time

#百度API语音接口
APP_ID = '19496104'
API_KEY = 'U5GgCantAC8euSH9hplgU7E2'
SECRET_KEY = 'yeeurU89BvMnqR3TyxLFGYOVUF1KgPUH'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
#字体
FONT_URL = './font/Alibaba-PuHuiTi-Heavy.ttf'

def make_text(text_1,text_2,text_3):
    text_i0 = '欢迎大家来到，看了也没用频道'
    text_i1 = text_1 + text_2 + '是怎么回事呢？'
    text_i2 = text_1 + '相信大家都很熟悉，但是' + text_i1
    text_i3 = '下面就让小编带大家一起了解一下吧。'
    text_i4 = text_1 + text_2 + '其实就是' + text_3
    text_i5 = '大家可能会很惊讶' + text_1 + '怎么会' + text_2 + '呢？'
    text_i6 = '但事实就是这样，小编也感到很惊讶。'
    text_i7 = '这就是关于' + text_1 + text_2 + '的事了，大家有什么看法呢？'
    text_i8 = '欢迎在评论区告诉小编，一起讨论哦！'
    text_i = [text_i0,text_i1,text_i2,text_i3,text_i4,text_i5,text_i6,text_i7,text_i8]
    return text_i

def make_music(text,spd):
    start = 2
    delay = 0.5
    music_clip = AudioFileClip('back.mp3').volumex(0.5)
    text_i = make_text(text[0],text[1],text[2])
    str_n = ''
    i = 1
    for text in text_i:
        result = client.synthesis(text=text, options={'vol': 5, 'per': 4, 'spd': spd})
        with open('audio.mp3', 'wb') as fy:
            fy.write(result)
        fy.close()
        time.sleep(0.5)

        # 加入独白
        audio_clip = AudioFileClip('audio.mp3').set_start(start)
        music_clip = CompositeAudioClip([music_clip, audio_clip])
        voice_file = eyed3.load('audio.mp3')
        temp_long = voice_file.info.time_secs
        # 秒数转时分秒
        m, s = divmod(start, 60)
        h, m = divmod(m, 60)
        str1 = "%02d:%02d:%2.3f" % (h, m, s)
        str1 = str1.replace('.', ',')
        start = start + temp_long
        m, s = divmod(start, 60)
        h, m = divmod(m, 60)
        str2 = "%02d:%02d:%2.3f" % (h, m, s)
        str2 = str2.replace('.', ',')
        str_n = str_n + str(i) + '\n' + str1 + '   -->   ' + str2 + '\n' + text + '\n' + '\n'
        i = i + 1
        start += delay
        time.sleep(0.5)
    #存储字幕文件
    with open('test.srt', 'w') as f:
        f.write(str_n)
    f.close()
    return (music_clip,start)

def make_video(text,spd):
    music_clip,end= make_music(text, spd)
    #打开srt字幕文件
    generator = lambda txt: TextClip(txt, font = FONT_URL,fontsize=40, color='white')
    sub = SubtitlesClip("test.srt",generator)

    end += 1
    #随机挑选素材中的视频部分
    a = []
    Name = 39    #视频个数 按1~n排列  .mp4结尾
    N= 6        # 随机选取的视频个数  最好总时长能达到1分钟   这里每个素材时长10s
    name = random.randint(1, Name)
    a.append(name)
    background_clip = VideoFileClip('movie/' + str(name) + '.mp4')
    for i in range(N-1):
        while 1:
            name = random.randint(1, Name)
            if name not in a:
                break
        a.append(name)
        clip_temp = VideoFileClip('movie/' + str(name) + '.mp4')
        background_clip = concatenate_videoclips([background_clip,clip_temp])
    background_clip = background_clip.set_audio(music_clip)
    background_clip = CompositeVideoClip([background_clip, sub.set_position(('center','bottom'))]).subclip(0,end)
    return background_clip

#导出视频
def out_video(background_clip):
    video = all.volumex(background_clip, 0.8)
    video.write_videofile('out.mp4')

def del_temp():
    ls = ['audio.mp3', 'test.srt']
    for x in ls:
        if os.path.exists(x):
            os.remove(x)
        else:
            print('文件已消失，无需删除。')

if __name__ == '__main__':
    title = "营销号视频制作V1.00~仓鼠二号制"
    text = []
    temp = g.enterbox("输入主体:",title)
    text.append(temp)
    temp = g.enterbox('输入事件:', title)
    text.append(temp)
    temp = g.enterbox('输入原因:', title)
    text.append(temp)
    spd = g.integerbox('输入语句速度（0~9）:', title)
    if spd < 0 :
        spd = 0
    elif spd>9:
        spd = 9
    g.msgbox('点击OK继续运行程序，请耐心等待，如长时间无响应关闭重启软件', title)
    out_video(make_video(text,spd))
    del_temp()
    g.msgbox('输出完成，请查看"out.mp4"文件',title)

