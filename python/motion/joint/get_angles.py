#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < get_angles.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/03 >
#	> Last Changed: 
#	> Description:		读取关节的角度
#################################################################

import argparse
from naoqi import ALProxy
import time

tts = motion = None

def main(robot_IP, robot_PORT=9559):
	# ----------> Connect to robot <----------
	global tts, motion
	tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
	motion = ALProxy("ALMotion", robot_IP, robot_PORT)

	# ----------> get angle <----------
#	myGetAngles('Body', False)
#	myGetAngles('Body', True) 		# 使用传感器检测会更加准确
#	myGetAngles('Joints', False)
	
	motion.setStiffnesses("Body", 1.0)
	while True:
		print motion.getAngles('HeadPitch', True)
		time.sleep(0.5)

def myGetAngles(names, useSensors):
	'''
		获取name中的关节名称及关节角度
		names: 			预设值名称; 'Body', 'JointActuators', 'Joints', 'Actuators'
		useSensors: 	是否使用传感器检测;
	'''
	print "getBodyNames() - ", names
	namelist = motion.getBodyNames(names)
	print "getAngles() - ", names, " - useSensors:", useSensors
	anglelist = motion.getAngles(names, useSensors)
	
	for i in range(len(namelist)):
		print "Name:", namelist[i], " - ", 'angle:', anglelist[i]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
