# /usr/bin/env python
# -*- coding:utf-8 -*-
# author: Handsome Lu  time:2020/4/19

from moviepy.editor import *
from moviepy.audio.fx import all
from moviepy.video.tools.subtitles import SubtitlesClip
import os
import time
import eyed3
import random
from aip import AipSpeech
#百度API语音接口
APP_ID = '你的ID'
API_KEY = '你的KEY'
SECRET_KEY = '自己需要在百度申请'
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
        if not isinstance(result, dict):
            with open('audio.mp3', 'wb') as fy:
                fy.write(result)
            fy.close()
        else:
            print(dict)
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

def make_video(text):
    spd = int(input('语句速度（0~9）:'))
    while 1:
        if spd < 0 or spd > 9:
            spd = int(input('重新输入语句速度（0~9）:'))
        else:
            break
    music_clip,end= make_music(text, spd)

    #打开srt字幕文件
    generator = lambda txt: TextClip(txt, font = FONT_URL,fontsize=30, color='white')
    sub = SubtitlesClip("test.srt",generator)

    end += 1
    #随机挑选素材中的视频部分
    a = []
    name = random.randint(1, 4)
    a.append(name)
    for i in range(2,4):
        while 1:
            name = random.randint(1, 4)
            if name not in a:
                break
        a.append(name)
    clip_1 = VideoFileClip('movie/' + str(a[0]) + '.mp4').subclip(0, random.randint(15,20))
    clip_2 = VideoFileClip('movie/' + str(a[1]) + '.mp4').subclip(0, random.randint(15,20))
    clip_3 = VideoFileClip('movie/' + str(a[2]) + '.mp4').subclip(0, random.randint(15,20))

    #合并3个视频片段，并加入声音
    background_clip = concatenate_videoclips([clip_1,clip_2,clip_3])
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
    text = []
    temp = input('输入主体:')
    text.append(temp)
    temp = input('输入事件:')
    text.append(temp)
    temp = input('输入原因:')
    text.append(temp)
    out_video(make_video(text))
    del_temp()

