import random
class Zombie:
    def __init__(self):
        self.Zombie_num=0#僵尸生成频率
        self.Zombie_Location_List=[]#僵尸列表
        self.x=1000
        self.life=2#僵尸初始生命值
        self.speed=2#僵尸初始移动速度
        self.Zombie_number=250#僵尸出现变量
        self.Zombie_Go_ballistic_time=0#暴走初始时间
        self.Zombie_Go_ballistic_time_max=2000#僵尸暴走时间

    def Creat_Zombie(self):#创建僵尸的坐标
        if self.Zombie_num>=self.Zombie_number and self.Zombie_num%self.Zombie_number==0:
            #Zombie_Location=[[x坐标，y坐标，生命值，初始行动状态（步行）]]
            Zombie_Location = [[self.x,75,self.life,0],[self.x,175,self.life,0],[self.x,275,self.life,0],[self.x,375,self.life,0],[self.x,475,self.life,0]]#僵尸生成位置
            rand=random.randint(0,4)
            self.Zombie_Location_List.append(Zombie_Location[rand])
            for i in self.Zombie_Location_List:
                if i[0]<=-50:#当僵尸坐标为-50时，删除僵尸
                    self.Zombie_Location_List.pop(self.Zombie_Location_List.index(i))
                    continue
            self.Zombie_num=0
            return self.Zombie_Location_List
        if self.Zombie_Location_List!=[]:#僵尸移动
            for i in self.Zombie_Location_List:
                i[0]-=self.speed
        self.Zombie_num+=1
        self.Zombie_Go_ballistic_time+=1
        if self.Zombie_Go_ballistic_time>self.Zombie_Go_ballistic_time_max:#暴走之后更新僵尸属性
            self.speed=10
            self.life=20
            self.Zombie_number=30
        return self.Zombie_Location_List