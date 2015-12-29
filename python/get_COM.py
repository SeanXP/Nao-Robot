#-*- coding: utf-8 -*-
from naoqi import ALProxy
import motion

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motionProxy = ALProxy("ALMotion", robot_ip, robot_port)

# ---------->  <----------

# Example showing how to get the COM position of "HeadYaw".
name = "HeadYaw"
frame = motion.FRAME_TORSO
useSensors = False
pos = motionProxy.getCOM(name, frame, useSensors)
print "HeadYaw COM Position: x = ", pos[0], " y:", pos[1], " z:", pos[2]

