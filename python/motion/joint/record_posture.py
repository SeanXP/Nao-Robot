#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < record_posture.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/03 >
#	> Last Changed: 
#	> Description:		记录机器人的姿势，并还原姿势
#################################################################

import argparse
from naoqi import ALProxy
import time

tts = motion = autonomous = None

posture = {}

def main(robot_IP, robot_PORT=9559):
	# ----------> Connect to robot <----------
	global tts, motion, autonomous
	tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
	motion = ALProxy("ALMotion", robot_IP, robot_PORT)
	autonomous = ALProxy("ALAutonomousLife", robot_IP, robot_PORT)
	autonomous.setState("disabled") # turn ALAutonomousLife off

	# ----------> <----------
	record()
	reappear()

def record():
	'''
		将机器人全身关节放松，等待用户设置姿势，设置姿势后记录所有关节值；
	'''
	# 蹲下再站立，保证安全
	motion.rest()
	motion.wakeUp()
	# 放松所有关节
	tts.say("rest all joints")
	motion.setStiffnesses("Body", 0.0) # 非僵硬状态，此时可任意改变机器人的姿态，程序控制无效。
	# 等待
	tts.say("wait 10 seconds.")
	time.sleep(10)
	# 锁定所有关节
	tts.say("lock all joints")
	motion.setStiffnesses("Body", 1.0) # 僵硬状态, 此时机器人的关节锁定，可以程序控制，不可人工移动。	
	# 记录关节数值
	tts.say('recording')
	namelist = motion.getBodyNames('Body')
	anglelist = motion.getAngles('Body', True)
	global posture
	for i in range(len(namelist)):
		posture[namelist[i]] = anglelist[i]
	# 记录完毕, 将机器人复位
	tts.say('ok, recorded.')
	print posture
	motion.rest()


def reappear():
	'''
		恢复记录的姿势
	'''
	motion.wakeUp()
	tts.say("reappear recorded posture")
	for name, angle in posture.items():
		print name, angle
		motion.post.setAngles(name, angle, 0.1)
	time.sleep(5)
	motion.rest()
	
def myGetAngles(names, useSensors):
	'''
		获取name中的关节名称及关节角度
		names:          预设值名称; 'Body', 'JointActuators', 'Joints', 'Actuators'
		useSensors:     是否使用传感器检测;
	'''
#	print "getBodyNames() - ", names
	namelist = motion.getBodyNames(names)
#	print "getAngles() - ", names, " - useSensors:", useSensors
	anglelist = motion.getAngles(names, useSensors)

#	debug, 打印输出
#	for i in range(len(namelist)):
#		print "Name:", namelist[i], " - ", 'angle:', anglelist[i]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
