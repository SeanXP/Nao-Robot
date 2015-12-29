#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < touch_passwd.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/27 >
#	> Last Changed: 
#	> Description:		Nao Robot touch password, 用于机器人触摸事件的编程练习；	
#################################################################

"""
	Nao Robot touch password, 用于机器人触摸事件的编程练习；
"""

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse

# 设定Head/Touch/Front=1,Head/Touch/Middle=2,Head/Touch/Rear=3
HEAD_FRONT = 1
HEAD_MIDDLE = 2
HEAD_REAR = 3

# 密码序列，只有按照下面序列依次触摸机器人，才会通过验证；
PASSWORD = [1,3,2,3,1,2]
PASSWD = []

VERIFY_FLAG = False			# 密码验证标志，成功验证时改为True

# Global variable to store the FrontTouch module instance
FrontTouch = None			# 密码序列：1
MiddleTouch = None			# 密码序列：2
RearTouch = None			# 密码序列：3
LeftFootTouch = None		# 确定密码
RightFootTouch = None		# 清空密码

tts = None
memory = None

class FrontTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
        # Subscribe to FrontTactilTouched event:
		memory.subscribeToEvent("FrontTactilTouched",
			"FrontTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		# Unsubscribe to the event when talking,
		# to avoid repetitions

		# value == 1.0, 即触摸响应；不考虑value == 0, 即离开触摸响应；
		# VERIFY_FLAG == False, 即未通过验证，此时才需要输入密码。验证后触摸无效；
		if value == 0 or VERIFY_FLAG == True:# 不符合条件，直接返回；这样可以有效防止事件未订阅异常
			return

		memory.unsubscribeToEvent("FrontTactilTouched",
			"FrontTouch")

		#if value == 1.0 and VERIFY_FLAG == False:
		PASSWD.append(HEAD_FRONT)
		tts.post.say("1")

			
        # Subscribe again to the event
		memory.subscribeToEvent("FrontTactilTouched",
			"FrontTouch",
			"onTouched")


class MiddleTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("MiddleTactilTouched",
			"MiddleTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		if value == 0 or VERIFY_FLAG == True:
			return
		memory.unsubscribeToEvent("MiddleTactilTouched",
			"MiddleTouch")

		PASSWD.append(HEAD_MIDDLE)
		tts.post.say("2")
			
		memory.subscribeToEvent("MiddleTactilTouched",
			"MiddleTouch",
			"onTouched")

class RearTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("RearTactilTouched",
			"RearTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		if value == 0 or VERIFY_FLAG == True:
			return
		memory.unsubscribeToEvent("RearTactilTouched",
			"RearTouch")

		PASSWD.append(HEAD_REAR)
		tts.post.say("3")
			
		memory.subscribeToEvent("RearTactilTouched",
			"RearTouch",
			"onTouched")

class LeftFootTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("LeftBumperPressed",
			"LeftFootTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		if value == 0 or VERIFY_FLAG == True:
			return
		memory.unsubscribeToEvent("LeftBumperPressed",
			"LeftFootTouch")
		
		global PASSWD
		tts.post.say("Confirm password.")
		verify(PASSWD)
		if VERIFY_FLAG == True: 	# 验证成功
			tts.post.say("OK! Welcome to Sword Art Online!")
		else:
			tts.post.say("No! Wrong password.")
		PASSWD = []	# 无论验证与否，都清空密码；
			
		memory.subscribeToEvent("LeftBumperPressed",
			"LeftFootTouch",
			"onTouched")

class RightFootTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("RightBumperPressed",
			"RightFootTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		'''	按右脚触摸，为清空密码；
   			在VERIFY_FLAG = False时，为清空密码；
  	 		而在VERIFY_FLAG = True时，为退出验证登录； 
			(退出登录功能，用于测试，为了保险，最后应该将此功能转为不易误触发的事件，例如胸前按钮三连击)
		'''
		if value == 0:
			return
		memory.unsubscribeToEvent("RightBumperPressed",
			"RightFootTouch")

		if VERIFY_FLAG == False:
			tts.post.say("Empty password.")
		else:
			tts.post.say("Logout.")
			global VERIFY_FLAG
			VERIFY_FLAG = False
		PASSWD = []
		memory.subscribeToEvent("RightBumperPressed",
			"RightFootTouch",
			"onTouched")

def	verify(passwd):
	'''	将用户输入的passwd与密码库PASSWORD对比
		验证成功则配置标志位VERIFY_FLAG=True;
		验证失败则VERIFY_FLAG=False
	'''
	global VERIFY_FLAG
	if len(PASSWORD) != len(passwd):
		VERIFY_FLAG = False	
	else:
		# 先设为True, 一旦有不相同的，立刻改为False
		VERIFY_FLAG = True
		for i in range(len(passwd)):
			if PASSWORD[i] != passwd[i]:	
				VERIFY_FLAG = False

def main(ip, port):
	""" Main entry point
	"""

	# We need this broker to be able to construct
	# NAOqi modules and subscribe to other modules
	# The broker must stay alive until the program exists
	
	myBroker = ALBroker("myBroker",
		"0.0.0.0",   # listen to anyone
		0,           # find a free port and use it
		ip,          # parent broker IP
		port)        # parent broker port

	global tts, memory
	tts = ALProxy("ALTextToSpeech", ip, port)
	memory = ALProxy("ALMemory", ip, port)

	global FrontTouch, MiddleTouch, RearTouch
	global LeftFootTouch, RightFootTouch
	FrontTouch = FrontTouch("FrontTouch")
	MiddleTouch = MiddleTouch("MiddleTouch")
	RearTouch = RearTouch("RearTouch")
	LeftFootTouch = LeftFootTouch("LeftFootTouch")
	RightFootTouch = RightFootTouch("RightFootTouch")

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print
		print "Interrupted by user, shutting down"
		myBroker.shutdown()
		sys.exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default="192.168.2.100",
						help="Robot ip address")
	parser.add_argument("--port", type=int, default=9559,
						help="Robot port number")
	args = parser.parse_args()
	main(args.ip, args.port)
