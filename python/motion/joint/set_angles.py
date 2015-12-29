#-*- coding: utf-8 -*-
from naoqi import ALProxy
import almath
import time


# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motionProxy = ALProxy("ALMotion", robot_ip, robot_port)
# ----------> 关节调整 <----------
motionProxy.setStiffnesses("Head", 1.0)

# Simple command for the HeadYaw joint at 10% max speed
names = "HeadYaw"
angles = 90.0 * almath.TO_RAD # 角度转弧度(almath.TO_RAD)
fractionMaxSpeed = 0.1
motionProxy.setAngles(names,angles,fractionMaxSpeed) # 以10%的速度转换angles角度
# setAngles()为非阻塞函数, 故需延时等待.
time.sleep(3.0)
motionProxy.setAngles(names,0,fractionMaxSpeed) # 以10%的速度转换angles角度
# 与changeAngles用法相同，唯一的区别是changeAngles()是相对弧度, setAngles为绝对弧度.
time.sleep(3.0)

# Example showing how to set angles, using a fraction of max speed
names  = ["HeadYaw", "HeadPitch"]
angles  = [0.2, -0.2] # 弧度
fractionMaxSpeed  = 0.1
motionProxy.setAngles(names, angles, fractionMaxSpeed)
time.sleep(3.0)


# Example showing a joint trajectory with a single destination
names = "HeadYaw"
angleLists = 1.0
times = 1.0
isAbsolute = True
motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)	
# 阻塞函数，一定时间内控制关节达到某目标位置；
# 角度和时间可以是List列表形式
# 参数4,isAbsolute=True则为绝对角度, False为相对当前位置的相对角度；

# Shake the head from side to side
names = "HeadYaw"
angleLists = [1.0, -1.0, 1.0, -1.0, 0.0]
times      = [1.0,  2.0, 3.0,  4.0, 5.0]
isAbsolute = True
motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)


motionProxy.setStiffnesses("Head", 0.0)
motionProxy.rest()
