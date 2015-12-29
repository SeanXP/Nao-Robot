#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < get_touch.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/27 >
#	> Last Changed: 
#	> Description:
#################################################################

import argparse
from naoqi import ALProxy
import time

def main(robot_IP, robot_PORT=9559):
	# ----------> Connect to robot <----------
	tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
	motion = ALProxy("ALMotion", robot_IP, robot_PORT)
#	posture = ALProxy("ALRobotPosture", robot_IP, robot_PORT)
#	memory = ALProxy("ALMemory", robot_IP, robot_PORT)
#	leds = ALProxy("ALLeds", robot_IP, robot_PORT)
#	battery = ALProxy("ALBattery", robot_IP, robot_PORT)
#	autonomous = ALProxy("ALAutonomousLife", robot_IP, robot_PORT)
#	autonomous.setState("disabled") # turn ALAutonomousLife off
	touch = ALProxy("ALTouch", robot_IP, robot_PORT)	

	# ----------> <----------
#	print touch.getSensorList()

#	output:
#	['Head/Touch/Front', 'Head/Touch/Middle', 'Head/Touch/Rear', 
#	'LHand/Touch/Back', 'LHand/Touch/Left', 'LHand/Touch/Right', 
#	'RHand/Touch/Back', 'RHand/Touch/Left', 'RHand/Touch/Right', 
#	'LFoot/Bumper/Left', 'LFoot/Bumper/Right', 
#	'RFoot/Bumper/Left', 'RFoot/Bumper/Right']

#	print touch.getStatus()

#	[
#		['Head', False, []], 
#		['LArm', False, []], 
#		['LLeg', False, []], ['RLeg', False, []], 
#		['RArm', False, []], 
#		['LHand', False, []], ['RHand', False, []], 
#		['Head/Touch/Front', False, []], ['Head/Touch/Middle', False, []], ['Head/Touch/Rear', False, []], 
#		['LFoot/Bumper/Left', False, []], ['LFoot/Bumper/Right', False, []], 
#		['RFoot/Bumper/Left', False, []], ['RFoot/Bumper/Right', False, []], 
#		['LHand/Touch/Left', False, []], ['LHand/Touch/Back', False, []], ['LHand/Touch/Right', False, []], 
#		['RHand/Touch/Left', False, []], ['RHand/Touch/Back', False, []], ['RHand/Touch/Right', False, []]
#	]	
#

#	间隔时间持续打印状态
#	该程序仅用于大概感受下机器人的触摸功能，若需要触摸即时性，准确性，应该使用TouchChanged事件
#		或其他事件进行捕捉触摸状态的改变。
	while True:
		status = touch.getStatus()
		counter = 0
		for e in status:
			if e[1] == True:
				print "No.",counter, e
			counter += 1
		print "----"
		time.sleep(0.2) # 这段事件触摸，机器人不会响应，因此实时性不高

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
