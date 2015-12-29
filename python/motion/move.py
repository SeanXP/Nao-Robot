#-*- coding: utf-8 -*-
from naoqi import ALProxy
import time

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559	# default port : 9559
motion = ALProxy("ALMotion", robot_ip, robot_port)
tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
posture = ALProxy("ALRobotPosture", robot_ip, robot_port)

tts.setLanguage("English")
# ----------> Make robot move <----------

# Wake up robot
# sets Motor on and, if needed, goes to initial position. 唤醒电机，必要时进入初始姿态。
# 对于H25 NAO Robot, 将设置stiffness为开启状态，并恢复起始站立状态;
# 执行了wakeUp(), 则无需执行motion.setStiffnesses("Body", 1.0)
motion.wakeUp()

# void ALMotionProxy::moveInit()
# Initializes the move process. Checks the robot pose and takes a right posture. This is blocking called.
# 初始化移动进程，检查机器人的姿势并切换为正确的姿势。调用此程序前需要打开电机(即wakeUp)，否则调用无效。
motion.moveInit()

# void ALMotionProxy::moveTo(const float& x, const float& y, const float& theta)
# Makes the robot move to the given pose in the ground plane, relative to FRAME_ROBOT. This is a blocking call.
# Parameters:	
#	x - Distance along the X axis in meters.
#	y - Distance along the Y axis in meters.
#	theta - Rotation around the Z axis in radians [-3.1415 to 3.1415].
# If moveTo() method does nothing on the robot, read the section about walk protection.
	
#移动位置是相对与FRAME_ROBOT的，因此如果机器人走到对应位置，下次调用相同moveTo()将无效果
#motion.moveTo(0.5, 0, 0) #阻塞调用，不并行
motion.post.moveTo(0.2, 0, 0) # 每个ALProxy代理都有post属性，通过它可以将程序变为后台运行，从而实现并行.	
tts.say("I am walking now")	  # 这里移动的同时，还要说话;
time.sleep(5)				  # 延时，使得机器人继续运动一段时间
motion.stopMove()	

# ----------> robot rest <----------
# 关闭电机，进入非僵硬模式，此后程序控制无效(因电机已关闭), 但可手工改变电机位置
# 进入复位状态(蹲伏动作)
tts.say("I am going to sleep")
motion.rest()
