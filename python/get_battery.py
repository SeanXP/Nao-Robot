#-*- coding: utf-8 -*-
from naoqi import ALProxy

''' 打印当前机器人的电量情况，单位: % 
'''
# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

batteryProxy = ALProxy("ALBattery", robot_ip, robot_port)

# ----------> get robot battery <----------

print "Robot battery charge(%):", batteryProxy.getBatteryCharge()
