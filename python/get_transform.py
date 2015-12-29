#-*- coding: utf-8 -*-
from naoqi import ALProxy
import motion
import argparse

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motionProxy = ALProxy("ALMotion", robot_ip, robot_port)

# ----------> get Transform and print <----------

# Example showing how to get the end of the right arm as a transform
# represented in torso space. The result is a 4 by 4 matrix composed
# of a 3*3 rotation matrix and a column vector of positions.

name  = 'RArm'
frame  = motion.FRAME_TORSO
useSensorValues  = True
result = motionProxy.getTransform(name, frame, useSensorValues)
for i in range(0, 4):
	for j in range(0, 4):
			print result[4*i + j],
	print ''

#R R R x
#R R R y
#R R R z
#0 0 0 1
