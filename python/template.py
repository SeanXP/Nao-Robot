#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < template.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/16 >
#	> Last Changed: 
#	> Description:		
#################################################################

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

	# ----------> <----------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
