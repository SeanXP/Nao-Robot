from naoqi import ALProxy
#-*- coding: utf-8 -*-

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559
motionProxy = ALProxy("ALMotion", robot_ip, robot_port)

# ----------> Set Joint <----------
names = "HeadYaw"			#各个关节的名称可以在sdk说明文档里找到
angleLists = [1.0,0.0]		#关节要转动的角度
timeLists = [1.0,2.0]		#到达指定角度的指定时间
isAbsoulte = True			#true代表绝对角度
#motionProxy.angleInterpolation(names,angleLists,timeLists,isAbsoulte)

# LShoulderRoll
# RShoulderRoll
#names = "HeadPitch"			
names = "LShoulderRoll"
angleLists = [1.0,0.0]	
timeLists = [1.0,2.0]
isAbsoulte = True	
motionProxy.angleInterpolation(names,angleLists,timeLists,isAbsoulte)

#names = "RShoulderRoll"
#motionProxy.angleInterpolation(names,angleLists,timeLists,isAbsoulte)
