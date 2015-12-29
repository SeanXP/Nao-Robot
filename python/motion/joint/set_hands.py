#-*- coding: utf-8 -*-
from naoqi import ALProxy
import time

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motionProxy = ALProxy("ALMotion", robot_ip, robot_port)
postureProxy = ALProxy("ALRobotPosture", robot_ip, robot_port)
# ----------> Set init Posture <----------
motionProxy.wakeUp()
#postureProxy.goToPosture("StandInit", 1)
# ----------> open hands<----------
motionProxy.openHand("LHand")
time.sleep(1)
motionProxy.closeHand("LHand")
time.sleep(1)

motionProxy.openHand("RHand")
time.sleep(1)
motionProxy.closeHand("RHand")
time.sleep(1)
