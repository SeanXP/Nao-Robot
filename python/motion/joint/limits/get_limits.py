#-*- coding: utf-8 -*-
from naoqi import ALProxy

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motionProxy = ALProxy("ALMotion", robot_ip, robot_port)

# Example showing how to get the limits for the whole body
name = "Body"
limits = motionProxy.getLimits(name)
jointNames = motionProxy.getBodyNames(name)
for i in range(0,len(limits)):
	print jointNames[i] + ":"
	print "minAngle", limits[i][0], "maxAngle", limits[i][1]
	print "maxVelocity", limits[i][2], "maxTorque", limits[i][3]
