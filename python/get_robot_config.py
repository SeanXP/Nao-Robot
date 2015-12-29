#-*- coding: utf-8 -*-
from naoqi import ALProxy

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motionProxy = ALProxy("ALMotion", robot_ip, robot_port)

# ----------> get robot config <----------
# Example showing how to get the robot config
robotConfig = motionProxy.getRobotConfig()
for i in range(len(robotConfig[0])):
	print robotConfig[0][i], ": ", robotConfig[1][i]



