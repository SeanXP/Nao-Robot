#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#	Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:		< sonar_module.py >
#	> Author:			< Sean Guo >		
#	> Mail:				< iseanxp+code@gmail.com >		
#	> Created Time:		< 2015/03/30 >
#	> Last Changed: 
#	> Description:
#################################################################

""" Print some messages  when receiving a ultrasonic event
	机器人超声波模块模块，订阅四个ultrasonic event，在终端打印出对应的信息；
"""

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse

# Global variable to store the ReactToTouch module instance
LeftDetected = None
RightDetected = None
LeftNothing = None
RightNothing = None

memory = None
sonar = None

class LeftDetected(ALModule):
	''' 左侧0.5米内有障碍
	'''
	def __init__(self, name):
		ALModule.__init__(self, name)
		# Subscribe to SonarLeftDetected event:
		memory.subscribeToEvent("SonarLeftDetected",
			"LeftDetected",
			"onDetected")
	# callback(std::string eventName, float distance, std::string subscriberIdentifier)
	def onDetected(self, eventName, distance):
		# Unsubscribe to the event when talking,
		# to avoid repetitions
		memory.unsubscribeToEvent("SonarLeftDetected",
			"LeftDetected")

		print "Left Detected:[", distance, "]"

		# Subscribe again to the event
		memory.subscribeToEvent("SonarLeftDetected",
			"LeftDetected",
			"onDetected")
class RightDetected(ALModule):
	''' 右侧0.5米内有障碍
	'''
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("SonarRightDetected",
			"RightDetected",
			"onDetected")
	def onDetected(self, eventName, distance):
		memory.unsubscribeToEvent("SonarRightDetected",
			"RightDetected")
		print "Right Detected:[", distance, "]"
		memory.subscribeToEvent("SonarRightDetected",
			"RightDetected",
			"onDetected")
class LeftNothing(ALModule):
	''' 左侧0.5米内无障碍
	'''
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("SonarLeftNothingDetected",
			"LeftNothing",
			"onDetected")
	def onDetected(self, eventName, distance):
		memory.unsubscribeToEvent("SonarLeftNothingDetected",
			"LeftNothing")
		print "Left Nothing:[", distance, "]"
		memory.subscribeToEvent("SonarLeftNothingDetected",
			"LeftNothing",
			"onDetected")
class RightNothing(ALModule):
	''' 右侧0.5米内无障碍
	'''
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("SonarRightNothingDetected",
			"RightNothing",
			"onDetected")
	def onDetected(self, eventName, distance):
		memory.unsubscribeToEvent("SonarRightNothingDetected",
			"RightNothing")
		print "Right Nothing:[", distance, "]"
		memory.subscribeToEvent("SonarRightNothingDetected",
			"RightNothing",
			"onDetected")

def main(ip, port):
	""" Main entry point
	"""
	# We need this broker to be able to construct
	# NAOqi modules and subscribe to other modules
	# The broker must stay alive until the program exists
	myBroker = ALBroker("myBroker",
		"0.0.0.0",	# listen to anyone
		0,			# find a free port and use it
		ip,			# parent broker IP
		port)		# parent broker port


	global memory, sonar
	memory = ALProxy("ALMemory", ip, port)
	sonar = ALProxy("ALSonar", ip, port)
	sonar.subscribe("SonarTestModule")

	global LeftDetected, RightDetected, LeftNothing, RightNothing
	LeftDetected = LeftDetected("LeftDetected")
	RightDetected = RightDetected("RightDetected")
	LeftNothing = LeftNothing("LeftNothing")
	RightNothing = RightNothing("RightNothing")

	try:
		while True:
			time.sleep(1)
#			print "Left Sonar:", memory.getData("Device/SubDeviceList/US/Left/Sensor/Value")
			print ""
	except KeyboardInterrupt:
		print
		print "Interrupted by user, shutting down"
		sonar.unsubscribe("SonarTestModule")
		myBroker.shutdown()
		sys.exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default="127.0.0.1",
						help="Robot ip address")
	parser.add_argument("--port", type=int, default=9559,
						help="Robot port number")
	args = parser.parse_args()
	main(args.ip, args.port)
