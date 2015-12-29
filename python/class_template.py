#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < class_template.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/14 >
#	> Last Changed: 
#	> Description:		类模板
#################################################################

from naoqi import ALProxy
import argparse
import threading        # 多线程类

class simple_class():
	'''
		创建类 - simple_class，功能为：
	'''
	def __init__(self, robot_ip, robot_port=9559):
		# 类成员变量

		# naoqi.ALProxy
		try:
			self.tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
		except Exception, e:
			print "Could not create proxy by ALProxy in Class MP3player"
			print "Error: ", e

		
class threading_class(threading.Thread):
    '''
		创建线程类 - threading_class，功能为：
	'''
	def __init__(self, robot_ip, robot_port=9559):
		# 线程类初始化
		threading.Thread.__init__(self)
		# 类成员变量

		# naoqi.ALProxy
		try:
			self.tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
		except Exception, e:
			print "Could not create proxy by ALProxy in Class MP3player"
			print "Error: ", e
	def run():
		pass
	def stop():
		pass

def main(robot_IP, robot_PORT=9559):
	# ----------> 实例化类 <----------
	myclass = threading_class(robot_IP, robot_PORT)
	myclass2 = simple_class(robot_IP, robot_PORT)

	try:
	# ----------> 测试用例 <----------
	myclass.start()
	
	except KeyboardInterrupt:
		# 中断程序
		myclass.stop()
		print "Interrupted by user, shutting down"
		sys.exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
	parser.add_argument("--port", type=int, default=9559, help="Robot port number")
	args = parser.parse_args()
	# ----------> 执行main函数 <----------
	main(args.ip, args.port)
