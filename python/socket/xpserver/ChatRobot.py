#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < ChatRobot.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/19 >
#	> Last Changed: 
#	> Description:		为NAO Robot实现的聊天机器人模块
#						内部使用其他聊天机器人的API;
#################################################################

import sys
import requests
try:
	# 从当前目录的settings.py中尝试读取Chat Robot API KEY
	# api key在聊天机器人的官网申请或购买;
	from settings import SIMSIMI_API_KEY, SIMSIMI_API_URL
	from settings import TULING_API_KEY, TULING_API_URL
except:
	SIMSIMI_API_KEY = ''
	SIMSIMI_API_URL = 'http://sandbox.api.simsimi.com/request.p'

	TULING_API_KEY = ''
	TULING_API_URL = 'http://www.tuling123.com/openapi/api'

class ChatRobot():
	def __init__(self):
		self.TULING_NAME = 'TULING'
		self.SIMSIMI_NAME = 'SIMSIMI'
		# 默认设置为图灵机器人引擎，后面可以再配置;
		self.robot = self.TULING_NAME
		self.api_url = TULING_API_URL 
		self.api_key = TULING_API_KEY

		self.session = requests.Session()

	def setRobot(self, robot):
		'''
			选择聊天机器人
		'''
		if robot == self.TULING_NAME:
			self.robot = self.TULING_NAME
			self.api_url = TULING_API_URL 
			self.api_key = TULING_API_KEY
		elif robot == self.SIMSIMI_NAME:
			self.robot = self.SIMSIMI_NAME
			self.api_url = SIMSIMI_API_URL 
			self.api_key = SIMSIMI_API_KEY
		else:
			print 'class ChatRobot::setRobot() - wrong robot name;'	
				
	def chat(self, message, language='ch'):
		try:
			if self.robot == self.SIMSIMI_NAME:
				# SimSimi
				payload = {'key':self.api_key, 'lc':language, 'ft':1.0, 'text':message}
				response = self.session.get(self.api_url, params=payload)
				answer = response.json()['response']
				return answer.encode('UTF-8')		# answer为unicode格式, 这里编码为str;
			elif self.robot == self.TULING_NAME:
				# Tuling
				payload = {'key':self.api_key, 'info':message}
				response = self.session.get(self.api_url, params=payload)
				answer = response.json()['text']
				return answer.encode('UTF-8')
			else:
				pass
		except:
			# 若json解析错误, 则返回预设回答
			return random.choice(['你真棒!', '真的嘛?', '然后呢~', '哦', '呵呵'])	

def main():
	chatrobot = ChatRobot()
#	chatrobot.setRobot('SIMSIMI')
	try:
		while True:
			megs = raw_input('输入:')
			answer = chatrobot.chat(megs)
			print answer
#			print type(answer)
	except KeyboardInterrupt:
		print ""
		print "Interrupted by user, shutting down"
		sys.exit()
if __name__ == '__main__':
	main()
