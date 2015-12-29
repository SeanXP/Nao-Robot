#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#	Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:		< sonar.py >
#	> Author:			< Sean Guo >		
#	> Mail:				< iseanxp+code@gmail.com >		
#	> Created Time:		< 2015/03/30 >
#	> Last Changed: 
#	> Description:		Nao robot - sonar
#################################################################

import argparse
import time
from naoqi import ALProxy
import sys

def main(robot_IP, robot_PORT=9559):
	# ----------> Connect to robot <----------
	try:
		tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
		motion = ALProxy("ALMotion", robot_IP, robot_PORT)
		memory = ALProxy("ALMemory", robot_IP, robot_PORT)
		sonar = ALProxy("ALSonar", robot_IP, robot_PORT)
	except Exception, e:
		print "Could not create proxy by ALProxy"
		print "Error was: ", e
	# ----------> <----------

	# Subscribe to sonars, this will launch sonars (at hardware level)
	# and start data acquisition.
	sonar.subscribe("myApplication")

	for i in range(100):
		# Now you can retrieve sonar data from ALMemory.
		# Get sonar left first echo (distance in meters to the first obstacle).
		print "Left Sonar:", memory.getData("Device/SubDeviceList/US/Left/Sensor/Value")
		# Same thing for right.
		print "Right Sonar:", memory.getData("Device/SubDeviceList/US/Right/Sensor/Value")
		print ""
		time.sleep(0.5)

	# Unsubscribe from sonars, this will stop sonars (at hardware level)
	sonar.unsubscribe("myApplication")

	# Please read Sonar ALMemory keys section
	# if you want to know the other values you can get.

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default="192.168.1.100", help="Robot ip address")
	parser.add_argument("--port", type=int, default=9559, help="Robot port number")
	args = parser.parse_args()
	# ----------> 执行main函数 <----------
	main(args.ip, args.port)
