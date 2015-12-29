#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < avoidance_module.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/08 >
#	> Last Changed: 	< 2015/04/13 >
#	> Description:		超声波避障模块
#						1.作为类使用，则import该文件，使用avoidance类; 用法见main();
#						2.也可直接python avoidance_module.py, 直接运行超声波避障功能;
#################################################################
"""
	超声波避障模块
"""
import sys
import time
import almath			# almath.TO_RAD, 角度转弧度
import argparse			# 参数解析
import threading    	# 多线程类
from naoqi import ALProxy

class avoidance(threading.Thread):
	'''
		创建线程类 - avoidance，实现超声波避障避障功能（线程类，可后台运行）
	'''
	def __init__(self, robot_ip, robot_port=9559):
		# 线程类初始化
		threading.Thread.__init__(self)
		# 障碍物标志
		self.obstacle_left = False 		# True则左侧有障碍
		self.obstacle_right = False  	# True则右侧有障碍
		self.run_flag = False			# 避障运行标志位，为False时表示退出避障循环
		# 障碍物全局变量
		self.check_distance = 0.5	# 设置检测的安全距离
		self.delay_seconds = 0.3	# 设置延时事件, 单位：秒
		self.move_speed = 0.4		# 移动速度, 单位: m/s
		self.turn_angle = 20		# 旋转角度，单位: 角度
		# naoqi.ALProxy
		try:
			self.motion = ALProxy("ALMotion", robot_ip, robot_port)
			self.memory = ALProxy("ALMemory", robot_ip, robot_port)
			self.sonar = ALProxy("ALSonar", robot_ip, robot_port)
		except Exception, e:
			print "Could not create proxy by ALProxy in Class avoidance"
			print "Error was: ", e

	def getflag(self):
		'''
			返回运行FLAG，为True表示正在运行, 为False表示停止工作;
		'''
		return self.run_flag
	def setflag(self, bools):
		'''
			设置运行FLAG, 从而控制避障功能的on/off;
		'''
		self.run_flag = bools
		return self.run_flag
	def run(self):
		''' 
			固定间隔循环检测是否存在障碍，根据障碍物标志决定机器人的行走方向
			通过设置run_flag标志位为False来停止。
		'''
		# 初始时设置运行标志位为True
		self.setflag(True)
		# 机器人行走初始化
		self.motion.wakeUp()
		self.motion.moveInit()
		# 订阅超声波
		self.sonar.subscribe("Class_avoidance")
		while self.run_flag == True:			# 避障标识为True，则持续循环检测
			# 1. 检测障碍物
			self.avoid_check()
			# 2. 根据障碍物标志决定行走方向
			self.avoid_operation()
			# 3. 延时
			time.sleep(self.delay_seconds)
		# 直到run_flag为False才会跳出while循环;
		# 取消订阅超声波
		self.sonar.unsubscribe("Class_avoidance")
		# 机器人复位
		self.motion.stopMove()
	def stop(self):
		self.setflag(False)
	def avoid_check(self):
		'''
			检测超声波数值，设置标志位
		'''
		left_value= self.memory.getData("Device/SubDeviceList/US/Left/Sensor/Value")
		right_value= self.memory.getData("Device/SubDeviceList/US/Right/Sensor/Value")
		if left_value> self.check_distance: 		# 超过安全距离，无障碍
			self.obstacle_left = False
		else:								# 小于安全距离，有障碍
			self.obstacle_left = True
		if right_value> self.check_distance: 		# 超过安全距离，无障碍
			self.obstacle_right = False
		else:								# 小于安全距离，有障碍
			self.obstacle_right = True
	def avoid_operation(self):
		# 	left		right				operation
		#   ----------------------------------------------
		# 	False		False				无障碍物，直走
		#	False		True				右侧障碍，左转
		#	True		False				左侧障碍，右转
		#	True		True				左右障碍，左转
		if self.obstacle_left == False:
			if self.obstacle_right == False:
				self.motion_go()
			else:
				self.motion_turn_left()
		else:
			if self.obstacle_right == False:
				self.motion_turn_right()
			else:
				self.motion_turn_left()
	def motion_go(self):
		self.motion.move(self.move_speed, 0, 0)
	def motion_turn_left(self):
		self.motion.post.moveTo(0, 0, self.turn_angle * almath.TO_RAD)
	def motion_turn_right(self):
		self.motion.post.moveTo(0, 0, -1.0 * self.turn_angle * almath.TO_RAD)

def main(robot_IP, robot_PORT=9559):
	# ----------> avoidance <----------
	avoid = avoidance(robot_IP, robot_PORT)
	try:
		avoid.start()					# start()只能执行一次, 会开新线程运行; 
										# run()可以多次执行, 但是会在本线程运行;
		# start()开新线程, 非阻塞, 因此这里延时一段时间以执行避障;
		time.sleep(10)
#		avoid.setflag(False)		 	# 方法1: 通过设置标志位为False来停止
		avoid.stop()					# 方法2: 通过调用stop()函数停止该线程类，其内部也是设置标志位.	

		# 想要再次开启避障，需要再新建一个类对象
		# 由于线程类只能调用start开启新线程一次，因此要多次使用超声波避障，需要实例化多个类；
		avoid2 = avoidance(robot_IP, robot_PORT)
		avoid2.start()
		time.sleep(10)
		avoid2.stop()
	except KeyboardInterrupt:
		# 中断程序
		avoid.stop()
		avoid2.stop()
		print "Interrupted by user, shutting down"
		sys.exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
	parser.add_argument("--port", type=int, default=9559, help="Robot port number")
	args = parser.parse_args()
	# ----------> 执行main函数 <----------
	main(args.ip, args.port)
