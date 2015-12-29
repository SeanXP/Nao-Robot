#-*- coding: utf-8 -*-
from naoqi import ALProxy

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motion = ALProxy("ALMotion", robot_ip, robot_port)

sensorList = motion.getSensorNames()
for sensor in sensorList:
	print sensor
