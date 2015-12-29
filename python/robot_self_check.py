#-*- coding: utf-8 -*-
from naoqi import ALProxy
import time
''' 一个模拟机器人自检的程序，机器人运动全身各个关节，假装自检。实际无自检效果。
'''
# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559	# default port : 9559
motion = ALProxy("ALMotion", robot_ip, robot_port)
tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)

tts.setLanguage("Chinese")
#tts.say("正在启动自检程序...")

#先复位
motion.rest() # 恢复复位姿态, 关闭电机会取消僵硬状态
#time.sleep(2.0)
#tts.say("正在进行头部检测...")
motion.setStiffnesses("HeadYaw", 1.0) # 打开电机，此时僵硬状态，可以程序控制机器人而人工不可移动关节
names = "HeadYaw"           #各个关节的名称可以在sdk说明文档里找到
angleLists = [-1.5,1.5]      #关节要转动的角度
timeLists = [3.0,6.0]       #到达指定角度的指定时间
isAbsoulte = True           #true代表绝对角度
motion.angleInterpolation(names,angleLists,timeLists,isAbsoulte)
angleLists = [1.5, -0.1]
timeLists = [1.0,3.0]
motion.angleInterpolation(names,angleLists,timeLists,isAbsoulte)
#tts.say("头部检测完毕")

#motion.wakeUp()
#tts.say("检测完毕，机器人完好无损，就地待命！")
