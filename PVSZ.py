#coding:utf-8
import pygame
from pygame.locals import *
from sys import exit
import time
import Main_Window
import Image
image=Image.Image()
pygame.mixer.init()#初始化音乐
pygame.mixer.music.load('jspvz/mian_audio/begin_window.mp3')#加载音乐
pygame.mixer.music.set_volume(0.7)	# 设置音量
buttonclick = pygame.mixer.Sound("jspvz/mian_audio/buttonclick.wav")#按钮音效
while True:
    window = Main_Window.Window()#创建窗口对象
    window.CreateWindow()
    if pygame.mixer.music.get_busy() == False:#判断当前是否有背景音乐正在播放
        pygame.mixer.music.play()#播放背景音乐
    for event in pygame.event.get():
        if event.type == QUIT:  # 接受到退出事件后退出程序
            exit()
        if event.type==KEYDOWN:#按下f开始
            if event.key==K_f:
                window.PlayGame()
        if event.type == pygame.MOUSEBUTTONDOWN :#检测鼠标按钮事件
            x1,y1=event.pos
            if 470<=x1<=800 and 96<=y1<=242:#判断点击位置
                buttonclick.play()
                begin1 = pygame.image.load(image.PlayGame2).convert_alpha()  # 开始按钮
                window.pywindow.blit(begin1, (470, 96))
                pygame.display.update()
                w, h=pygame.image.load(image.PlayGame1).convert_alpha().get_size()
                time.sleep(0.5)
                if window.is_rect(event.pos, (470, 100, w, h/2)):
                    pygame.mixer.music.stop()
                    window.PlayGame()
            if 800 <= x1 <= 900 and 500 <= y1 <= 550:#退出按钮
                if window.is_rect(event.pos, (800,500 ,50 , 50)):
                    exit()