#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < touch_password.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/14 >
#	> Last Changed: 
#	> Description:		touch password system
#						基于NAO机器人触摸传感器实现的登录系统;
#						用touchPasswd类包装;
#################################################################
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse
import time
import sys

# 必须使用全局变量作为类的实例化对象，否则事件触发后，ALModule找不到对应的类实例对象；
touchSystem = None

class touchPasswd(ALModule):
	'''
		创建类 - touchPasswd, 基于NAO机器人触摸传感器实现的登录系统;
		基类为Naoqi - ALModule, 在touchPasswd类中，订阅触摸事件;
	'''
	def __init__(self, name):
		# 基类初始化
		ALModule.__init__(self, name)
		self.name = name		# 记录实例的名称；订阅事件时要用到;
		# ----------> 类成员变量 <----------
		# 为机器人头部三块触摸区域指定编码;
		# 		Head/Touch/Front	=1
		#		Head/Touch/Middle	=2
		#		Head/Touch/Rear		=3
		self.HEAD_FRONT = 1
		self.HEAD_MIDDLE = 2
		self.HEAD_REAR = 3
		# 密码序列，只有按照下面序列依次触摸机器人，才会通过验证；
		# 密码元素: 单个数字、字符；后面语音反馈，机器人需要念出密码元素;
		self.password = [1,3,2,3,1,2]
		# 记录用户的输入密码，最后用来与正确密码做比较；
		self.input_passwd = []
		# 验证标志, 输入正确密码会设置标志为True; 默认为False;
		self.verify_flag = False
		
		# naoqi.ALProxy
		try:
			# 语音反馈
			self.tts = ALProxy("ALTextToSpeech")
			# 触摸事件订阅
			self.memory = ALProxy("ALMemory")
		except Exception, e:
			print "Could not create proxy by ALProxy in Class MP3player"
			print "Error: ", e

		# 订阅触摸事件
		# ALMemoryProxy::subscribeToEvent()
		#		参数1: 订阅事件名称; 
		#		参数2: 回调模块名称; 这里为具体的实例的名称，而非类名；
		#		参数3: 回调函数名称;
		self.memory.subscribeToEvent("FrontTactilTouched",
									self.name,
									"FrontTouched")
		self.memory.subscribeToEvent("MiddleTactilTouched",
									self.name,
									"MiddleTouched")
		self.memory.subscribeToEvent("RearTactilTouched",
									self.name,
									"RearTouched")
		self.memory.subscribeToEvent("LeftBumperPressed",
									self.name,
									"LeftFootTouched")
		self.memory.subscribeToEvent("RightBumperPressed",
									self.name,
									"RightFootTouched")
		# 使用事件:'ALChestButton/DoubleClickOccurred'作为退出登录按钮;
		# 由于此事件默认被'ALAutonomousLife'模块使用，这里需要注销;	
		sub_list = self.memory.getSubscribers('ALChestButton/DoubleClickOccurred')
		# sub_list 为订阅该事件的订阅者, 这里一一取消订阅;
		for sub in sub_list:
			self.memory.unsubscribeToEvent('ALChestButton/DoubleClickOccurred', sub)
		# 然后touchPasswd类订阅该事件
		self.memory.subscribeToEvent("ALChestButton/DoubleClickOccurred",
									self.name,
									"DoubleClick")

	def isVerify(self):
		'''返回是否通过验证'''
		return self.verify_flag
	def verify(self):
		''' 将用户输入密码input_passwd与系统密码password对比
			验证成功则配置标志位VERIFY_FLAG=True;
			验证失败则VERIFY_FLAG=False
		'''
		if self.input_passwd == self.password:
			# 密码正确，则设置标志位
			self.verify_flag = True
			self.tts.say("OK! Login in system.")
		else:
			# 密码错误，则设置标志位并清空密码
			self.verify_flag = False
			self.input_passwd = []
			self.tts.say("No! Wrong password.")
	def setPassword(self, password='132312'):
		'''
			设置密码
			参数: password, 字符串密码; 例如: "123321123"
		'''
		# 清空旧密码
		self.password = []
		# 加入新密码
		for i in range(len(password)):
			self.password.append(int(password[i]))
	def skipVerify(self):
		'''跳过验证，即无需输入密码，直接设置verify_flag为True;'''
		self.verify_flag = True
		self.tts.say('skip verify')

	# 回调函数:
	# Event: "FrontTactilTouched"
	# callback(std::string eventName, float val, std::string subscriberIdentifier)
	# 参数: eventName, 事件名称; val, 为1.0表示触摸, 为0表示没有触摸;
	# 触摸会产生val = 1.0的触摸事件; 松开触摸还会产生val = 0的触摸事件; 根据val的值区分;
	def FrontTouched(self, eventName, value):
		# value == 0, 即松开触摸事件，这里忽略；
		# verify_flag == True，即已通过验证，无需再输入密码，这里忽略；
		if value == 0 or self.verify_flag == True:
			return
		else:
			# 未通过验证且为触摸事件(value == 1)
			# 先取消订阅，避免回调函数多次调用冲突;
			self.memory.unsubscribeToEvent("FrontTactilTouched", self.name)

			self.input_passwd.append(self.HEAD_FRONT)
			self.tts.post.say(str(self.HEAD_FRONT))

			# Subscribe again to the event
			self.memory.subscribeToEvent("FrontTactilTouched",
									self.name,
									"FrontTouched")
	def MiddleTouched(self, eventName, value):
		if value == 0 or self.verify_flag == True:
			return
		else:
			self.memory.unsubscribeToEvent("MiddleTactilTouched", self.name)

			self.input_passwd.append(self.HEAD_MIDDLE)
			self.tts.post.say(str(self.HEAD_MIDDLE))

			self.memory.subscribeToEvent("MiddleTactilTouched",
									self.name,
									"MiddleTouched")
	def RearTouched(self, eventName, value):
		if value == 0 or self.verify_flag == True:
			return
		else:
			self.memory.unsubscribeToEvent("RearTactilTouched", self.name)

			self.input_passwd.append(self.HEAD_REAR)
			self.tts.post.say(str(self.HEAD_REAR))

			self.memory.subscribeToEvent("RearTactilTouched",
									self.name,
									"RearTouched")
	def LeftFootTouched(self, eventName, value):
		if value == 0 or self.verify_flag == True:
			return
		else:
			self.memory.unsubscribeToEvent("LeftBumperPressed", self.name)

			# Left Foot 确认密码
			self.tts.post.say('Confirm password.')
			self.verify()

			self.memory.subscribeToEvent("LeftBumperPressed",
									self.name,
									"LeftFootTouched")
	def RightFootTouched(self, eventName, value):
		''' 按右脚触摸，为清空密码；
			在VERIFY_FLAG = False时，为清空密码；
		'''
		if value == 0 or self.verify_flag == True:
			return
		else:
			self.memory.unsubscribeToEvent("RightBumperPressed", self.name)

			# Right Foot 清空密码
			self.tts.post.say('Empty password.')
			self.input_passwd = []

			self.memory.subscribeToEvent("RightBumperPressed",
									self.name,
									"RightFootTouched")
	def DoubleClick(self, eventName):
		'''
			对应事件：机器人胸前按钮二连击；
			对应功能：注销登录；
		'''
		if self.verify_flag == False:
			# 未通过验证, 则无需注销, 直接返回
			return
		# 注销操作
		# 先取消订阅，避免回调函数多次调用冲突;
		self.memory.unsubscribeToEvent("ALChestButton/DoubleClickOccurred", self.name)

		self.verify_flag = False
		self.tts.post.say('Log out.')

		# Subscribe again to the event
		self.memory.subscribeToEvent("ALChestButton/DoubleClickOccurred",
								self.name,
								"DoubleClick")
def main(robot_IP, robot_PORT=9559):

	# We need this broker to be able to construct NAOqi modules and subscribe to other modules
	# The broker must stay alive until the program exists

	myBroker = ALBroker("myBroker", 
						"0.0.0.0",   # listen to anyone
						0,           # find a free port and use it
						robot_IP,    # parent broker IP
						robot_PORT)  # parent broker port

	# ----------> touch password system <----------
	# 使用具体的类实例名称来初始化类;
	global touchSystem
	touchSystem = touchPasswd("touchSystem")
	touchSystem.setPassword('123')
#	touchSystem.skipVerify()			# 直接跳过验证;
	try:
		# 没有通过验证，则一直循环等待;
		while touchSystem.isVerify() == False:
			time.sleep(1)
		print 'verify succeed, exit!'
	except KeyboardInterrupt:
		# 中断程序
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
