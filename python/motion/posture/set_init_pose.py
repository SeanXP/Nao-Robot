#-*- coding: utf-8 -*-
from naoqi import ALProxy

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motionProxy = ALProxy("ALMotion", robot_ip, robot_port)
postureProxy = ALProxy("ALRobotPosture", robot_ip, robot_port)
# ----------> Set init Posture <----------
motionProxy.wakeUp()
postureProxy.goToPosture("StandInit", 1)
