#! /usr/bin/env python
#-*- coding: utf-8 -*-
from naoqi import ALProxy

# ----------> Connect to robot <----------
robot_ip = "192.168.2.100"
robot_port = 9559			# default port : 9559

motion = ALProxy("ALMotion", robot_ip, robot_port)

# ----------> something to do <----------
motion.rest()
