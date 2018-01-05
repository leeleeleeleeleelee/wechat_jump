#! /usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
from time import sleep
from PIL import Image

def pull_pic():
    #adb手机截图，保存在1.png
    os.system('adb shell screencap -p /sdcard/1.png')
    os.system('adb pull /sdcard/1.png')

def find_bot(im):
    #寻找棋子的位置
    x_sum = 0
    n = 0
    y_max = 0

    w,h = im.size
    pic = im.load()
    global a
    for y in range(h/3,2*h/3,5):
        for x in range(1,w):
            now_pixel = pic[x,y]
            if (50 < now_pixel[0] < 60) and (53 < now_pixel[1] < 63) and (95 < now_pixel[2] < 110):
                x_sum += x
                n += 1
                y_max = max(y,y_max)
    try:
        bot_x = x_sum / n
    except ZeroDivisionError:
        sys.exit('=============== 游戏已退出！===============')

    bot_y = y_max
    return (bot_x,bot_y)
    # aaa = im.crop((bot_x-5,bot_y-25,bot_x+5,bot_y-10))
    # aaa.show()

def find_target(im):
    #若下一个为矩形，寻找他的中心
    a = []
    sum_x = 0
    num_x = 0
    top_y = None
    w, h = im.size
    pic = im.load()
    for y in range(h/3,2*h/3,5):
        init_pixel = pic[0,y]
        for x in range(0,w):
            now_pixel = pic[x,y]
            if (now_pixel<>init_pixel) and ((now_pixel[0] not in range(50,63)) \
                    or (now_pixel[1] not in range(53,63)) and (now_pixel[2] not in range(95,110))):

                if top_y == None:
                    top_y = y
                    sum_x += x
                    num_x += 1
                elif top_y == y:
                    sum_x += x
                    num_x += 1
                elif top_y <> y:
                    break

    target_x =  sum_x/num_x

    ww = []
    target_pixel = pic[target_x,top_y][:3]
    for i in range(top_y,top_y+140):
        for m in range(0,w):
            if (target_pixel[0]-10 <= pic[m,i][0] <= target_pixel[0]+10) and \
                    (target_pixel[1]-10 <= pic[m,i][1] <= target_pixel[1]+10) and \
                    (target_pixel[2]-10 <= pic[m,i][2] <= target_pixel[2]+10) :
                ww.append((m,i))
                break
    www = sorted(ww,key=lambda x:x[0])
    target_y = www[0][1]+4

    return (target_x,target_y)



num = 0
while True:
    num += 1
    print u'第%s次跳跃'%num
    pull_pic()
    im = Image.open('./1.png')
    bot_x,bot_y = find_bot(im)
    print u'棋子坐标：',(bot_x,bot_y)
    target_x,target_y = find_target(im)
    print u'目标方块中心坐标',(target_x,target_y)
    x_dis = abs(bot_x-target_x)
    y_dis = abs(bot_y-target_y)
    distance = (x_dis**2 + y_dis**2)**0.5
    press = distance * 1.365
    print u'按压力度：',press
    cmd = 'adb shell input swipe 20 20 20 20 '+str(int(press))
    os.system(cmd)
    print '-'*40
    sleep(1)

