# /usr/bin/env python
# -*- coding:utf-8 -*-
# author: Handsome Lu  time:2020/4/24
from moviepy.editor import *
from moviepy.audio.fx import all
from moviepy.video.tools.subtitles import SubtitlesClip
import os
import eyed3
import random
from aip import AipSpeech
import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import back_ui
import threading

#百度API语音接口
APP_ID = '1'
API_KEY = '1'
SECRET_KEY = ''

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
#字体
FONT_URL = './font/Alibaba-PuHuiTi-Heavy.ttf'


def get_music(text,spd,voice):
    result = client.synthesis(text=text, options={'vol': 5, 'per': voice, 'spd': spd})
    with open('audio.mp3', 'wb') as fy:
        fy.write(result)
    fy.close()

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

def make_music(text,spd,back_music,voice):
    start = 2
    delay = 0.5
    if back_music < 1 or back_music > 6:
        music_name = 'music/'+ str(random.randint(1,6))+'.mp3'
    else:
        music_name = 'music/' + str(back_music) + '.mp3'
    music_clip = AudioFileClip(music_name).volumex(0.6)

    text_i = make_text(text[0],text[1],text[2])
    str_n = ''
    i = 1
    for text in text_i:
        get_music(text,spd,voice)
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

def make_video(text,spd,back_music,voice):
    music_clip,end= make_music(text, spd,back_music,voice)
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


class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        text1 = ui.lineEdit.text()
        text2 = ui.lineEdit_2.text()
        text3 = ui.lineEdit_3.text()
        text = [text1, text2, text3]
        spd = ui.spinBox.value()
        voice = ui.comboBox.currentIndex()
        back_music = ui.comboBox_2.currentIndex()
        out_video(make_video(text, spd, back_music, voice))
        del_temp()
        ui.pushButton.setText('开始')
        ui.pushButton.setDisabled(0)

def work():
    TT = myThread(1)
    ui.pushButton.setDisabled(1)
    ui.pushButton.setText('请等待，长时间无反应重启软件。。。。')
    myThread(1).start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = back_ui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.pushButton.clicked.connect(work)
    sys.exit(app.exec_())
