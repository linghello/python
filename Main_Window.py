#coding:utf-8
import pygame
from pygame.locals import *
from sys import exit
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EV
import Image
import time
import Botany
import Zombie
import Collision
import Audio
class Window:
    def __init__(self):
        self.pywindow=pygame.display.set_mode((900, 600), 0, 32)#窗口大小
        self.image=Image.Image()#导入图片
        self.botany=Botany.Botany()#植物类
        self.zombie=Zombie.Zombie()#僵尸类
        self.collision=Collision.Collision()#碰撞类
        self.audio=Audio.Audio()#音频类
        self.Sunny_Collect=[]#回收的阳光坐标列表
        self.Sunny_Collect_x=0
        self.Sunny_Collect_y=0
        self.Botany_Type=0#植物类型
        self.Botany_Animation_Type=0#植物动画类型
        self.Zombie_Animation_Type=0#僵尸动画类型
        self.Stop_image=self.image.game_pause_nor#暂停初始图标
        self.Zombie_image_list=0#僵尸图片列表索引
        self.SunFlower_image_list=16#向日葵图片列表索引(从后往前索引只是想测试一下，并无大碍）
        self.Peashooter_image_list=12#豌豆列表索引
        self.ZombieAttack_image_list=0#僵尸吃植物索引
        self.FootballZombie_image_list=0#重装僵尸图片索引
        self.FootballZombieAttack_image_list=0#重装僵尸吃植物图片索引
        self.FootballZombieDie_image_list=0#重装僵尸死亡图片索引
        self.evillaugh=pygame.mixer.Sound(self.audio.evillaugh)#僵尸暴走音效
        self.Zombie_Go_ballistic_audio=0#暴走音效控制变量
        self.scream=pygame.mixer.Sound(self.audio.scream)#僵尸胜利音效
        self.buttonclick = pygame.mixer.Sound(self.audio.buttonclick)  # 按钮音效
        self.Zdie=pygame.mixer.Sound(self.audio.groan4)#僵尸死亡音效
        self.ZWon=0#僵尸胜利后音效控制
    def CreateWindow(self):#开始窗口
        pygame.init()  # 初始化窗口
        pygame.display.set_caption("植物大战僵尸")
        begin = pygame.image.load(self.image.Surface).convert_alpha()
        self.pywindow.blit(begin, (0, 0))
        begin1 = pygame.image.load(self.image.PlayGame1).convert_alpha()#开始冒险吧图片
        self.pywindow.blit(begin1, (470, -50))
        pygame.display.update()
    def GameWindow(self):#游戏窗口
        begin1 = pygame.image.load(self.image.background1).convert_alpha()
        self.pywindow.blit(begin1, (-180, 0))
        SeedBank = pygame.image.load(self.image.SeedBank).convert_alpha()
        self.pywindow.blit(SeedBank, (0, 0))
        Myfont = pygame.font.SysFont("", 30)
        sunny_text = Myfont.render(str(self.botany.sunny_number), True, (0, 0, 0))#阳光数量文本
        self.pywindow.blit(sunny_text, (30, 65))
        stop = pygame.image.load(self.Stop_image).convert_alpha()
        self.pywindow.blit(stop, (850, 0))
        Shovel = pygame.image.load(self.image.Shovel).convert_alpha()
        self.pywindow.blit(Shovel, (450, 0))
    def Botany_show(self):#植物召唤区
        if self.botany.sunny_number<50:#判断阳光数量，加载不同的图片
            botany = pygame.image.load(self.image.SunFlowerfb).convert_alpha()
            self.pywindow.blit(botany, (80, 5))
            WallNutfb = pygame.image.load(self.image.WallNutfb).convert_alpha()
            self.pywindow.blit(WallNutfb, (200, 5))
        if self.botany.sunny_number>=50:
            botany = pygame.image.load(self.image.SunFlower).convert_alpha()
            self.pywindow.blit(botany, (80, 5))
            WallNut = pygame.image.load(self.image.WallNut).convert_alpha()
            self.pywindow.blit(WallNut, (200, 5))
        if self.botany.sunny_number<100:
            botany = pygame.image.load(self.image.PeaShooterfb).convert_alpha()
            self.pywindow.blit(botany, (140, 5))
        if self.botany.sunny_number>=100:
            botany = pygame.image.load(self.image.PeaShooter).convert_alpha()
            self.pywindow.blit(botany, (140, 5))
    def Produce_System_sunny(self):#加载生成的阳光图片
        sun=self.botany.Produce_sunny()#该方法返回生成的阳光坐标列表
        if sun!=[]:
            for i in sun:
                    sun = pygame.image.load(self.image.Sun).convert_alpha()
                    self.pywindow.blit(sun, (i[0], i[1]))
    def Collect_Sunny(self,pos):#收取阳光
        #1,点击阳光2.阳光增加3.坐标出栈4,加载动画
        w, h = pygame.image.load(self.image.Sun).convert_alpha().get_size()#获取阳光图片的大小
        for i in self.botany.Sunny_location:
            if self.is_rect(pos, (i[0], i[1], w, h )):
                self.botany.Delete_sunny(i[0],i[1])#删除植物对象里阳光的坐标
                self.Sunny_Collect.append([i[0], i[1]])#在新的列表里增加阳光的坐标
    def Sunny_Collect_Animation(self):#阳光回收动画
        if self.Sunny_Collect!=[]:#如果阳光列表不为空
            for i in self.Sunny_Collect:
                if self.Sunny_Collect_x==0 and self.Sunny_Collect_y==0:#计算动画加载的距离
                    self.Sunny_Collect_x=int(i[0]*0.1)
                    self.Sunny_Collect_y=int(i[1]*0.1)
                i[0]-=self.Sunny_Collect_x
                i[1]-=self.Sunny_Collect_y
                Sunny_Collect = pygame.image.load(self.image.Sun).convert_alpha()
                self.pywindow.blit(Sunny_Collect, (i[0], i[1]))
                if i[0]<=10:#当阳光回收后，删除阳光坐标
                    self.Sunny_Collect.pop(self.Sunny_Collect.index([i[0],i[1]]))
                    self.Sunny_Collect_x=0
                    self.Sunny_Collect_y=0
    def Plant_Botany_Type(self,pos):#植物种植类型
         if self.Botany_Type==0:
             self.Botany_Type=self.botany.Plant_Botany_Type(pos)#获取要种植的植物类型
    def Plant_Botany_Animation(self,pos):#点击植物后植物跟随鼠标移动
        x,y=pos#当前鼠标的坐标
        #根据要种植的植物类型，在鼠标上加载相应的图片
        if self.Botany_Type==1 and self.botany.sunny_number>=50:
            sun = pygame.image.load(self.image.SunFlower1).convert_alpha()
            self.pywindow.blit(sun, (x-32, y-36))
        if self.Botany_Type==2 and self.botany.sunny_number>=100:
            Peashooter = pygame.image.load(self.image.Peashooter1).convert_alpha()
            self.pywindow.blit(Peashooter, (x-32, y-36))
        if self.Botany_Type==3 and self.botany.sunny_number>=50:
            Peashooter = pygame.image.load(self.image.WallNut1).convert_alpha()
            self.pywindow.blit(Peashooter, (x-30, y-35))
        if self.Botany_Type==666:#铲子
            Shovel = pygame.image.load(self.image.Shovel).convert_alpha()
            self.pywindow.blit(Shovel, (x-40, y-40))
    def Plant_Botany(self):#植物种植在地上
        for i in self.botany.Plant_Botany_List:#遍历植物种植列表，在相应的位置加载图片
            if i[2]==1:
                sun = pygame.image.load(self.image.SunFlower_list[self.SunFlower_image_list]).convert_alpha()
                self.pywindow.blit(sun, (i[0], i[1]))
            if i[2] == 2:
                Peashooter = pygame.image.load(self.image.Peashooter_list[self.Peashooter_image_list]).convert_alpha()
                self.pywindow.blit(Peashooter, (i[0], i[1]))
            if i[2] == 3:
                if i[3]>=50:#根据坚果血量改变图片
                    WallNut1 = pygame.image.load(self.image.WallNut1).convert_alpha()
                    self.pywindow.blit(WallNut1, (i[0], i[1]))
                elif i[3]>=20:
                    Wallnut_cracked1 = pygame.image.load(self.image.Wallnut_cracked1).convert_alpha()
                    self.pywindow.blit(Wallnut_cracked1, (i[0], i[1]))
                else:
                    Wallnut_cracked2 = pygame.image.load(self.image.Wallnut_cracked2).convert_alpha()
                    self.pywindow.blit(Wallnut_cracked2, (i[0], i[1]+5))
        self.SunFlower_image_list-=1
        self.Peashooter_image_list-=1
        if self.SunFlower_image_list==-1:
            self.SunFlower_image_list=16
        if self.Peashooter_image_list==-1:
            self.Peashooter_image_list=12
    def Botany_Lab_Location(self):#显示植物子弹位置
        for i in self.botany.Botany_Lab():#子弹坐标
            bullet11 = pygame.image.load(self.image.ProjectilePea).convert_alpha()
            self.pywindow.blit(bullet11, (i[0]+63, i[1]))
    def Creat_Zombie_Location(self):#僵尸出现
        xxxx = self.zombie.Creat_Zombie()
        for i in xxxx:
            if i != []:
                if i[3]==0:#判断僵尸初始移动状态，0为步行，其他为吃植物
                    if self.zombie.Zombie_Go_ballistic_time<=self.zombie.Zombie_Go_ballistic_time_max:
                        bullet = pygame.image.load(self.image.Zombiez_list[self.Zombie_image_list]).convert_alpha()
                        self.pywindow.blit(bullet, (i[0], i[1]-30))
                    else:
                        FootballZombielist = pygame.image.load(self.image.FootballZombie_list[self.FootballZombie_image_list]).convert_alpha()
                        self.pywindow.blit(FootballZombielist, (i[0], i[1] - 30))
                else:
                    if self.zombie.Zombie_Go_ballistic_time<=self.zombie.Zombie_Go_ballistic_time_max:
                        bullet = pygame.image.load(self.image.ZombieAttack_list[self.ZombieAttack_image_list]).convert_alpha()
                        self.pywindow.blit(bullet, (i[0]-5, i[1] - 30))
                    else:
                        if 4<=self.FootballZombieAttack_image_list<=6:
                            FootballZombieAttacklist = pygame.image.load(
                                self.image.FootballZombieAttack_list[
                                    self.FootballZombieAttack_image_list]).convert_alpha()
                            self.pywindow.blit(FootballZombieAttacklist, (i[0]+10, i[1] - 30))
                        elif self.FootballZombieAttack_image_list==8:
                            FootballZombieAttacklist = pygame.image.load(
                                self.image.FootballZombieAttack_list[
                                    self.FootballZombieAttack_image_list]).convert_alpha()
                            self.pywindow.blit(FootballZombieAttacklist, (i[0]+5, i[1] - 30))
                        else:
                            FootballZombieAttacklist = pygame.image.load(
                                self.image.FootballZombieAttack_list[self.FootballZombieAttack_image_list]).convert_alpha()
                            self.pywindow.blit(FootballZombieAttacklist, (i[0], i[1] - 30))
        self.Zombie_image_list+=1
        self.ZombieAttack_image_list+=1
        self.FootballZombie_image_list+=1
        self.FootballZombieAttack_image_list+=1
        if self.Zombie_image_list==30:
            self.Zombie_image_list=0
        if self.ZombieAttack_image_list==21:
            self.ZombieAttack_image_list=0
        if self.FootballZombie_image_list==11:
            self.FootballZombie_image_list=0
        if self.FootballZombieAttack_image_list==10:
            self.FootballZombieAttack_image_list=0
    def Zombie_Go_ballistic(self):#僵尸暴走提示
        if self.zombie.Zombie_Go_ballistic_time_max<=self.zombie.Zombie_Go_ballistic_time<=self.zombie.Zombie_Go_ballistic_time_max+25:
            if self.Zombie_Go_ballistic_audio==0:
                self.evillaugh.play()
                self.Zombie_Go_ballistic_audio+=1
            LargeWave = pygame.image.load(self.image.LargeWave).convert_alpha()
            self.pywindow.blit(LargeWave, (307, 283))
    def Zombie_Ruin_Location(self):# 在僵尸死亡位置播放动画
        for i in self.collision.Collision_Testing(self.botany.Lab,self.zombie.Zombie_Location_List):
            # 根据摧毁坐标播放相应动画,该方法返回值是僵尸死亡列表
            if i != []:
                if self.zombie.Zombie_Go_ballistic_time<=self.zombie.Zombie_Go_ballistic_time_max:#判断僵尸是否暴走
                    if i[2]==0:
                        self.Zdie.set_volume(10)
                        self.Zdie.play()#播放僵尸死亡音效
                        ZombieDie = pygame.image.load(self.image.ZombieDie_list[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0], i[1]))
                    if i[2]==1:
                        ZombieDie = pygame.image.load(self.image.ZombieDie_list[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]-12, i[1]+22))
                    if i[2]==2:
                        ZombieDie = pygame.image.load(self.image.ZombieDie_list[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]-15, i[1]+19))
                    if i[2]==3:
                        ZombieDie = pygame.image.load(self.image.ZombieDie_list[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]-37, i[1]+18))
                    if i[2]==4:
                        ZombieDie = pygame.image.load(self.image.ZombieDie_list[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]-61, i[1]+20))
                    if i[2]==5:
                        ZombieDie = pygame.image.load(self.image.ZombieDie_list[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]-73, i[1]+22))
                    if i[2]==6:
                        ZombieDie = pygame.image.load(self.image.ZombieDie_list[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]-87, i[1]+38))
                    if i[2]==7:
                        ZombieDie = pygame.image.load(self.image.ZombieDie_list[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]-100, i[1]+51))
                    if i[2]==8:
                        ZombieDie = pygame.image.load(self.image.ZombieDie_list[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]-112, i[1]+52))
                    if i[2]==9:
                        ZombieDie = pygame.image.load(self.image.ZombieDie_list[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]-112, i[1]+53))
                    i[2]+=1
                    if(i[2]>=10):
                        self.collision.Zombie_Ruin.pop(self.collision.Zombie_Ruin.index(i))
                else:
                    if i[2]==0:#122,137
                        self.Zdie.play()
                        ZombieDie = pygame.image.load(self.image.FootballZombieDie[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]+12, i[1]-20))
                    if i[2]==1:
                        ZombieDie = pygame.image.load(self.image.FootballZombieDie[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0]+6, i[1]+27))
                    if i[2]==2:
                        ZombieDie = pygame.image.load(self.image.FootballZombieDie[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0], i[1]+29))
                    if i[2]==3:
                        ZombieDie = pygame.image.load(self.image.FootballZombieDie[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0], i[1]+20))
                    if i[2]==4:
                        ZombieDie = pygame.image.load(self.image.FootballZombieDie[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0], i[1]+25))
                    if i[2]==5:
                        ZombieDie = pygame.image.load(self.image.FootballZombieDie[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0], i[1]+25))
                    if i[2]==6:
                        ZombieDie = pygame.image.load(self.image.FootballZombieDie[i[2]]).convert_alpha()
                        self.pywindow.blit(ZombieDie, (i[0], i[1]+19))
                    i[2] += 1
                    if (i[2] >= 7):
                        self.collision.Zombie_Ruin.pop(self.collision.Zombie_Ruin.index(i))
    def Zombies_Won(self):#僵尸胜利
        for i in self.zombie.Zombie_Location_List:
            if i[0]<=0:
                return False
        return True
    def Stop(self,pos):#暂停
        w, h = pygame.image.load(self.Stop_image).convert_alpha().get_size()
        if self.is_rect(pos,(850,0,w,h)):
            self.buttonclick.play()
            while True:
                self.GameWindow()  # 创建游戏窗口
                self.Stop_image=self.image.game_resume_nor
                stop = pygame.image.load(self.Stop_image).convert_alpha()
                self.pywindow.blit(stop, (850, 0))
                blhx = pygame.image.load(self.image.blhx).convert_alpha()
                self.pywindow.blit(blhx, (183, 150))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:  # 接受到退出事件后退出程序
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:  # 点击继续开始
                        if self.is_rect(event.pos, (850, 0, w, h)):
                            self.buttonclick.play()
                            self.Stop_image = self.image.game_pause_nor
                            break
                if self.Stop_image == self.image.game_pause_nor:
                    break
    def is_rect(self,pos, rect):  # 计算图片的点击区域(继续按钮)
        x, y = pos#点击的位置
        rx, ry, rw, rh = rect
        if (rx <= x <= rx + rw) and (ry <= y <= ry + rh):
            return True
        return False

    def PlayGame(self):#主程序
        pygame.init()  # 初始化窗口
        pygame.mixer.init()  # 初始化音乐
        pygame.mixer.music.load(self.audio.Faster)  # 加载音乐
        # pygame.mixer.music.set_volume(0.7)#控制音量
        self.pywindow = pygame.display.set_mode((900, 600), 0, 32)
        pygame.display.set_caption("植物大战僵尸")
        clock = pygame.time.Clock()  # 刷新变量
        while True:
            self.GameWindow()#创建游戏窗口
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.play()
            for event in pygame.event.get():
                if event.type == QUIT:  # 接受到退出事件后退出程序
                    exit()
                if event.type == KEYDOWN:  # 按下f开始
                    if event.key == K_f:#f修改阳光，修改为5000
                        self.botany.sunny_number=5000
                    if event.key==K_x:#x把僵尸暴走时间设置为1000个运行周期之后
                        self.zombie.Zombie_Go_ballistic_time_max=1000
                if event.type == pygame.MOUSEBUTTONDOWN:#检测鼠标事件
                    pressed_array = pygame.mouse.get_pressed()#得到鼠标按钮状态，返回一个序列代表所有mousebuttons状态的布尔值。
                    for index in range(len(pressed_array)):
                        if pressed_array[index]:
                            if index==0:#当鼠标左键按下值为0
                                self.Collect_Sunny(event.pos)  # 点击阳光
                                self.Plant_Botany_Type(event.pos)  # 设置植物类型
                                self.Botany_Type = self.botany.Plant_Botany_location(event.pos)  # 获取植物类型
                                self.Stop(event.pos)  # 暂停
                            elif index==2:#鼠标右键按下时值为2
                                self.Botany_Type=0#重置植物种植类型
                                self.botany.Type=0
            self.Botany_show()#显示植物召唤区
            self.Sunny_Collect_Animation()#显示太阳回收动画
            self.Plant_Botany_Animation(pygame.mouse.get_pos())#获取当前鼠标位置、、点击植物后植物跟随鼠标移动
            self.Plant_Botany()#植物种植
            self.Produce_System_sunny()#生产的阳光图片
            self.Botany_Lab_Location()#植物子弹的位置
            self.Creat_Zombie_Location()#生成僵尸
            self.Zombie_Go_ballistic()#僵尸暴走提示
            self.Zombie_Ruin_Location()#显示僵尸死亡动画
            self.collision.Zombie_Eat_Botany(self.botany.Plant_Botany_List,self.zombie.Zombie_Location_List,self.zombie.Zombie_Go_ballistic_time,self.zombie.Zombie_Go_ballistic_time_max)#僵尸吃植物
            if self.Zombies_Won()==False:
                pygame.mixer.music.stop()#关闭背景音乐
                pygame.mixer.music.load(self.audio.Look_up_at_the_Sky)#僵尸胜利后背景音乐
                time.sleep(1)
                break
            clock.tick(60)
            pygame.display.update()
        while True:
            if self.ZWon==0:
                self.scream.play()#大叫
                self.ZWon+=1
            ZombiesWon = pygame.image.load(self.image.ZombiesWon).convert_alpha()
            self.pywindow.blit(ZombiesWon, (160, 66))
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.play()#播放僵尸胜利后背景音乐
            for event in pygame.event.get():
                if event.type == QUIT:  # 接受到退出事件后退出程序
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()  # 关闭背景音乐
                break
            pygame.display.update()