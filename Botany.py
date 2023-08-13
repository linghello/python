#coding:utf-8
import random
class Botany:
    def __init__(self):
        self.sunny_number=50#阳光数量
        self.System_produce_sunny_time=0#太阳系统生成时间
        self.Sunny_location=[]#阳光位置
        self.Plant_Botany_List=[]#植物种植列表
        self.Type=0#1.向日葵2.豌豆3.坚果666.铲子
        self.Lab_num=0#子弹生成
        self.Lab=[]#子弹坐标
        self.WanDou_life=5#生命值
        self.XiangRiKui_life=5#向日葵生命值
        self.JianGuo_life=100#坚果生命值
        self.Lab_num_time=30#子弹生成控制量
    def Produce_sunny(self):# 生成阳光
        for i in self.Plant_Botany_List:
            if i[2]==1:#植物类型为向日葵时(1为向日葵）
                i[4]+=1
                if i[4] >= 150 and i[4] % 150 == 0:#判断阳光变量
                    self.Sunny_location.append([i[0], i[1], 1,i[1]])
                    i[4]=0
        if self.System_produce_sunny_time>=150 :#当系统时间大于150时生成一个阳光
            x = random.randint(200,800)
            y = -200
            self.Sunny_location.append([x,y,0])
            self.System_produce_sunny_time=0

        for i in self.Sunny_location:
            if i[2]==0:#当阳光类型为系统阳光时，掉落的y=300的坐标会停止往下掉
                if i[1]<=300:
                    i[1]+=10
            if i[2]==1:#当阳光类型为向日葵的阳光时，掉落到当前向日葵坐标+30
                if i[1]-30<i[3]:
                    i[1]+=10
        self.System_produce_sunny_time+=1#增加系统时间
        return self.Sunny_location
    def Delete_sunny(self,x,y):#根据鼠标点击位置（x，y）销毁阳光坐标，增加阳光数量
        try:
            self.Sunny_location.pop(self.Sunny_location.index([x,y,0]))
        except:
            pass
        try:
            self.Sunny_location.pop(self.Sunny_location.index([x,y,1,y-30]))
        except:
            pass
        self.sunny_number+=25
    def Plant_Botany_Type(self,pos):#种植植物类型
        #1.点击植物获取信息2.移动时获取图片3.种植时生成坐标列表
        x, y = pos#点击的位置
        rx, ry, rw, rh = 80,5,49,75#向日葵卡片的位置
        rx1,ry1,rw1,rh1=140,5,50,75#豌豆卡片位置
        rx2,ry2,rw2,rh2=450,0,80,80#铲子卡片位置
        rx3,ry3,rw3,rh3=200,5,50,75#坚果卡片位置
        if (rx <= x <= rx + rw) and (ry <= y <= ry + rh) and self.sunny_number>=50:
            self.Type=1
            return self.Type#返回种植类型
        if (rx1 <= x <= rx1 + rw1) and (ry1 <= y <= ry1 + rh1) and self.sunny_number>=100:
            self.Type=2
            return self.Type
        if (rx3 <= x <= rx3 + rw3) and (ry3 <= y <= ry3 + rh3) and self.sunny_number>=50:
            self.Type=3
            return self.Type
        if (rx2 <= x <= rx2 + rw2) and (ry2 <= y <= ry2 + rh2):
            self.Type=666#铲子编号
            return self.Type
        return self.Type
    def Plant_Botany_location(self,pos):#((72X80,100+75X100)植物种植
        x,y=pos#鼠标坐标
        if self.Type!=0:
            if 72<=x<=792 and 100<=y<=575:
                if x<80:#计算相应的区域，然后种植植物
                    location_x=72+10
                else:
                    location_x=(int(x/80)-1)*80+72+10
                location_y=(int((y+25)/100)-1)*100+75+10
                if self.Type!=666:#666铲子类型
                    if self.Plant_Botany_List!=[]:
                        for i in self.Plant_Botany_List:
                            if i[0]==location_x and i[1]==location_y:
                                return self.Type
                if self.Type==1:
                    self.Plant_Botany_List.append([location_x,location_y,1,self.XiangRiKui_life,0])
                    self.Type=0
                    self.sunny_number-=50
                if self.Type==2:
                    self.Plant_Botany_List.append([location_x, location_y, 2,self.WanDou_life])
                    self.Type = 0
                    self.sunny_number -= 100
                if self.Type==3:
                    self.Plant_Botany_List.append([location_x, location_y, 3,self.JianGuo_life])
                    self.Type = 0
                    self.sunny_number -= 50
                if self.Type==666:#铲子
                    for i in self.Plant_Botany_List:
                        if i[0]==location_x and i[1]==location_y:
                            self.Plant_Botany_List.pop(self.Plant_Botany_List.index(i))#铲除植物
                            self.Type = 0
                return self.Type
        return self.Type
    def Botany_Lab(self):# 生成子弹位置
        if self.Lab_num>=self.Lab_num_time and self.Lab_num%self.Lab_num_time==0:#豌豆子弹频率
            for i in self.Plant_Botany_List:
                if i[2]==2:#当植物类型为豌豆时
                    self.Lab.append([i[0],i[1]])#在豌豆位置创建子弹
                    self.Lab_num=0
        for i in self.Lab:
            if i[0]>=800:#子弹坐标大于800时删除子弹
                self.Lab.pop(self.Lab.index(i))
                continue
            i[0]+=10
        self.Lab_num+=1
        return self.Lab


