#-*- coding: utf-8 -*-
from naoqi import ALProxy
import time

''' 
监视机器人的电量。每秒打印一次电量。
'''
# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

batteryProxy = ALProxy("ALBattery", robot_ip, robot_port)

# ----------> get robot battery <----------
while(True):
	print "Robot battery charge(%):", batteryProxy.getBatteryCharge()
	time.sleep(1)
