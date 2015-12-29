#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < mute.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/03 >
#	> Last Changed: 
#	> Description:			
#################################################################

'''
	判断，如果非静音，则设置机器人扬声器为静音；
		  如果是静音，则取消静音；
'''

import argparse
from naoqi import ALProxy

tts = motion = posture = memory = leds = battery = autonomous = None

def main(robot_IP, robot_PORT=9559):
	global tts, motion, posture, memory, leds, battery, autonomous
	# ----------> Connect to robot <----------
	tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
	motion = ALProxy("ALMotion", robot_IP, robot_PORT)
#	posture = ALProxy("ALRobotPosture", robot_IP, robot_PORT)
#	memory = ALProxy("ALMemory", robot_IP, robot_PORT)
#	leds = ALProxy("ALLeds", robot_IP, robot_PORT)
#	battery = ALProxy("ALBattery", robot_IP, robot_PORT)
#	autonomous = ALProxy("ALAutonomousLife", robot_IP, robot_PORT)
#	autonomous.setState("disabled") # turn ALAutonomousLife off
	audio = ALProxy("ALAudioDevice", robot_IP, robot_PORT)

	# ----------> Mute <----------
	if audio.isAudioOutMuted() == False:
		tts.say('mute')
		audio.muteAudioOut(True)
	else:
		audio.muteAudioOut(False)
		tts.say('unmute')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
