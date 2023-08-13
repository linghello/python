import pygame
class Collision:
    def __init__(self):
        pygame.mixer.init()  # 初始化音乐
        self.Zombie_Ruin=[]#僵尸死亡坐标
        self.Botany_Ruin=[]#植物死亡坐标
        self.chi_autio=pygame.mixer.Sound("jspvz/mian_audio/chi.wav")#吃植物音效
        self.chi_autio.set_volume(0.5)
        self.lab = pygame.mixer.Sound("jspvz/mian_audio/lab.wav")#子弹音效
    def Collision_Testing(self,Lab,Zombie):#子弹射僵尸
        for x in Lab:  # 遍历子弹列表和僵尸列表的坐标
            for y in Zombie:
                if y!=[]:
                    if y[0]-60<=x[0]<= y[0] and y[1] <= x[1] <= y[1] + 60:
                        self.lab.play()
                        if y[2] == 0:  # 检查生命值，为0则删除僵尸
                            self.Zombie_Ruin.append([y[0],y[1],0])
                            try:
                                Lab.pop(Lab.index(x))  # 删除子弹坐标
                            except:
                                pass
                            try:
                                Zombie.pop(Zombie.index(y))  # 删除僵尸坐标
                            except:
                                pass
                        else:
                            try:
                                Lab.pop(Lab.index(x))# 删除子弹坐标
                            except:
                                pass
                            y[2] -= 1
        return self.Zombie_Ruin
    def Zombie_Eat_Botany(self,Botany_Location,Zombie_Location,Zombie_Go_ballistic_time,Zombie_Go_ballistic_time_max):#僵尸吃植物
        for i in Botany_Location:#遍历植物和僵尸的列表
            for x in Zombie_Location:
                if i[0]<=x[0]<i[0]+60 and i[1]-10<=x[1]<i[1]+50:
                    i[3]-=1
                    if Zombie_Go_ballistic_time<=Zombie_Go_ballistic_time_max:
                        x[0] += 2
                    else:
                        x[0]+=10
                    x[3]=1
                    self.chi_autio.play()
                    if i[3]<=0:#当植物生命值为0时
                        x[3] = 0
                        try:
                            Botany_Location.pop(Botany_Location.index(i))#删除植物
                        except:
                            pass