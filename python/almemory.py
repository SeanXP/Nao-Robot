from naoqi import ALProxy
#-*- coding: utf-8 -*-

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

almemory = ALProxy("ALMemory", robot_ip, robot_port)
pings = almemory.ping()
print "ALMemory.ping():", pings
