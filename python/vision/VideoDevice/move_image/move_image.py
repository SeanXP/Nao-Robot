#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < move_image.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/05/04 >
#	> Last Changed: 
#	> Description:		Nao robot move and take picture.
#						控制机器人边避障行走，边旋转头部拍照。
#						
#################################################################

import time
import sys      # sys.exit() 退出main函数
import almath   # 角度转弧度(almath.TO_RAD)
import thread   # 多线程
import time     # 延时函数 time.sleep(1)
from optparse import OptionParser

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

# 自定义Python Module
from avoidance_module import *			# 超声波避障模块
from video_image import *				# 拍照模块 

ROBOT_IP = '192.168.2.100'
ROBOT_PORT = 9559

#-------------------> 全局变量 <-----------------
avoid = image = None

def main():
	# ----------> 命令行解析 <----------
	global ROBOT_IP
	parser = OptionParser()
	parser.add_option("--pip",
		help="Parent broker port. The IP address or your robot",
		dest="pip")
	parser.add_option("--pport",
		help="Parent broker port. The port NAOqi is listening to",
		dest="pport",
		type="int")
	parser.set_defaults(
		pip=ROBOT_IP,
		pport=9559)

	(opts, args_) = parser.parse_args()
	pip   = opts.pip
	pport = opts.pport
	# 如果运行前指定ip参数，则更新ROBOT_IP全局变量;
	# 其他模块会用到ROBOT_IP变量;
	ROBOT_IP = pip

	# ----------> 创建python broker <----------
	myBroker = ALBroker("myBroker",
		"0.0.0.0",   # listen to anyone
		0,           # find a free port and use it
		pip,         # parent broker IP
		pport)       # parent broker port


	# ----------> 创建Robot ALProxy Module<----------
	global tts, motion, autonomous
	tts = ALProxy("ALTextToSpeech")
	# 默认为英语语言包
	tts.setLanguage("English")
	motion = ALProxy("ALMotion")
	# turn ALAutonomousLife off
	autonomous = ALProxy("ALAutonomousLife")
	autonomous.setState("disabled") 			

	# ----------> 自己实现的类 <----------
	global avoid
	avoid = avoidance(ROBOT_IP, ROBOT_PORT) 	# 超声波避障类
	
	global video
	video = VideoImage(ROBOT_IP, ROBOT_PORT)	# 拍照类

	try:
		video.addXtionCamera()
		video.subscribeCamera()
		video.setCamera(0)
		# 开启线程避障
		avoid.start()
		video.takeRGBDimage(1000)
	except KeyboardInterrupt:
		print
		print "Interrupted by user, shutting down"
		avoid.stop()				# 关闭避障
		video.close()				# 关闭视频传输模块
		myBroker.shutdown()			# 关闭代理Broker
		sys.exit(0)

if __name__ == "__main__":
	main()
