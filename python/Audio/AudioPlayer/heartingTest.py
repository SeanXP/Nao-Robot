#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < heartingTest.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/30 >
#	> Last Changed: 
#	> Description:		人耳频率测试
#################################################################

import argparse
from naoqi import ALProxy
import time
import sys

def main(robot_IP, robot_PORT=9559):
	# ----------> Connect to robot <----------
	aup = ALProxy("ALAudioPlayer", robot_IP, robot_PORT)
	# ----------> play music <----------
	aup.stopAll()
	print "hearting High HZ test..."
	print "Press CTRL+C when you can not hear"
	try:
		high_hz = 1000				
		while True:
			aup.playSine(high_hz, 30, 0, 1)
			time.sleep(1)
			aup.stopAll()
			high_hz = high_hz + 500
		aup.stopAll()
	except KeyboardInterrupt:
		aup.stopAll()
		print ""
		print "High HZ:", high_hz
	
	aup.stopAll()
	time.sleep(1)
	print "hearting Low HZ test..."
	print "Press CTRL+C when you can not hear"
	try:
		low_hz = 1000				
		while True:
			aup.playSine(low_hz, 30, 0, 1)
			time.sleep(1)
			aup.stopAll()
			if low_hz <= 0:
				print "0 HZ"
				aup.stopAll()
				sys.exit()
			elif low_hz <= 200:
				low_hz = low_hz - 20
			else:
				low_hz = low_hz - 100
		aup.stopAll()
	except KeyboardInterrupt:
		aup.stopAll()
		print ""
		print "Low HZ:", low_hz
		print "Hearing frequency range:[", low_hz, ",", high_hz, "]"
		sys.exit()
	

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
