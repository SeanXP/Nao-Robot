#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < leds.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/28 >
#	> Last Changed:		< 2015/04/15 > 
#	> Description:		Nao robot led control
#################################################################

import argparse
from naoqi import ALProxy
import time
import random
import sys
import thread           # 多线程

# 关于流水灯、眨眼、变色等操作，由于执行事件过长, 建议使用thread多线程调用;

# Naoqi ALProxy 
leds = None

# 全局变量
LED_EAR_FLUSH_UNTIL_FLAG = False
LED_FACE_FLUSH_UNTIL_FLAG = False

# ----------> Face Led List <----------
FaceLedList = ["FaceLed0", "FaceLed1", "FaceLed2", "FaceLed3", 
			   "FaceLed4", "FaceLed5", "FaceLed6", "FaceLed7"]
# ----------> Ear Led List <----------
RightEarLedList = ["RightEarLed1", "RightEarLed2", "RightEarLed3", "RightEarLed4", 
				   "RightEarLed5", "RightEarLed6", "RightEarLed7", "RightEarLed8",
				   "RightEarLed9", "RightEarLed10"]
LeftEarLedList = ["LeftEarLed1", "LeftEarLed2", "LeftEarLed3", "LeftEarLed4", 
				  "LeftEarLed5", "LeftEarLed6", "LeftEarLed7", "LeftEarLed8",
				  "LeftEarLed9", "LeftEarLed10"]
# ----------> Color List <----------
ColorList = ['red', 'white', 'green', 'blue', 'yellow', 'magenta', 'cyan'] # fadeRGB()的预设值

def main(robot_IP, robot_PORT=9559):
	try:
		# ----------> Connect to robot <----------
		global leds
		leds = ALProxy("ALLeds", robot_IP, robot_PORT)
		# ----------> Led control <----------
#		print 'face led test...'
#		print 'face on'
#		LED_face_ON(leds)
#		time.sleep(1)
#		print 'face off'
#		LED_face_OFF(leds)
#		time.sleep(1)
#		print 'face flush 5 times'
#		LED_face_Flush(leds, 5)
#		time.sleep(1)
#		print 'face blink 5 times'
#		LED_face_Blink(leds, 5)
#		time.sleep(1)
#		print 'set face color to', ColorList[0]
#		LED_face_Color(leds, ColorList[0])
#		time.sleep(1)
#		print 'set face color to', ColorList[1]
#		LED_face_Color(leds, ColorList[1])
#		time.sleep(1)
#
#		print 'ear led test...'
#		print 'ear on'
#		LED_ear_ON(leds)
#		time.sleep(1)
#		print 'ear off'
#		LED_ear_OFF(leds)
#		time.sleep(1)
#		print 'ear flush 5 times'
#		LED_ear_Flush(leds, 5)
#		time.sleep(1)
#
#		print 'thread test'
#		thread.start_new_thread(LED_face_Flush, (leds, 10))
#		thread.start_new_thread(LED_ear_Flush, (leds, 10))
#		print 'wait thread over'
#		time.sleep(5)
#		print 'test over'
		
		print 'LED_ear_Flush_Until() test'
		print 'set flag True'
		setEarFlushFlag(True)
		setFaceFlushFlag(True)
		thread.start_new_thread(LED_ear_Flush_Until, (leds,)) 
		thread.start_new_thread(LED_face_Flush_Until, (leds,)) 
		
		time.sleep(10)
		print 'set flag False'
		setEarFlushFlag(False)
		setFaceFlushFlag(False)
		time.sleep(10)
	except KeyboardInterrupt:
		print ""
		print 'Interrupted by user, shutting down'
		sys.exit(0)


def LED_face_ON(ledsProxy):
	'''
		打开Face LED
	'''
	ledsProxy.on("FaceLeds")
def LED_face_OFF(ledsProxy):
	'''
		关闭Face LED
	'''
	ledsProxy.off("FaceLeds")
def LED_ear_ON(ledsProxy):
	ledsProxy.on("EarLeds")
def LED_ear_OFF(ledsProxy):
	ledsProxy.off("EarLeds")

def LED_face_Flush(ledsProxy, number=1, duration=0.05):
	'''
		在duration时间间隔下, 按顺序依次打开/关闭LED, 实现流水灯闪烁效果。
		number, 闪烁次数
		duration, 间隔事件，控制闪烁速度
	'''
	for num in range(number):
		# open face leds
		for index in range(len(FaceLedList)):
			ledsProxy.fade(FaceLedList[index], 1, duration)
		# close face leds
		for index in range(len(FaceLedList)):
			ledsProxy.fade(FaceLedList[index], 0, duration)
	
def LED_face_Blink(ledsProxy, number=1, duration=0.2):
	'''
		机器人眨眼睛
		duration, 眨眼速度
		number, 眨眼次数
	'''
	LedValueList = [0, 0, 1, 0,
					0, 0, 1, 0]
	# blink face leds
	for num in range(number):
		# 关闭一些LED, 实现眨眼效果;
		for i in range(len(FaceLedList)):
			ledsProxy.post.fade(FaceLedList[i], LedValueList[i], duration)
		# 延时，视觉停留效应
		time.sleep(0.1) 	
		# 重新打开所有LED
		ledsProxy.fade("FaceLeds", 1, duration)
		
def LED_face_RandomColor(ledsProxy, number=5, duration=1):
	"""
		The color of the eyes changes randomly.
		number, 次数；
		duration, 随机颜色切换事件, 速度;
	"""
	for i in range(number):
		rRandTime = random.uniform(0.0, 2.0) #随机速度
		ledsProxy.fadeRGB("FaceLeds", 
			256 * random.randint(0,255) + 256*256 * random.randint(0,255) + random.randint(0,255),
			rRandTime)
		time.sleep(random.uniform(0.0, duration))

def LED_face_Color(ledsProxy, color='white', duration=0.1):
	"""
		change the color of the eyes to [color].
		color, 颜色；
		duration, 间隔事件, 速度;
	"""
	for led in FaceLedList:
		ledsProxy.post.fadeRGB(led, color, duration)
def LED_face_SwitchColor(ledsProxy, color='white', delay=3, duration=0.1):
	'''
		以duration的速度切换到color颜色，等待delay秒后再切换会白色;
	'''
	LED_face_Color(ledsProxy, color, duration)
	time.sleep(delay)
	LED_face_Color(ledsProxy, 'white', duration)

def LED_ear_ON(ledsProxy):
	ledsProxy.on('EarLeds')
def LED_ear_OFF(ledsProxy):
	ledsProxy.off('EarLeds')

def LED_ear_Flush(ledsProxy, number=10, duration=0.05):
	"""
		number, 闪烁次数
		duration, 闪烁速度
	"""
	for num in range(number):
		for i in range(len(RightEarLedList)):
			ledsProxy.fade(LeftEarLedList[i], 1, duration)
			ledsProxy.fade(RightEarLedList[i], 1, duration)
		for i in range(len(RightEarLedList)):
			ledsProxy.fade(LeftEarLedList[i], 0, duration)
			ledsProxy.fade(RightEarLedList[i], 0, duration)

def setEarFlushFlag(bools):
	global LED_EAR_FLUSH_UNTIL_FLAG
	LED_EAR_FLUSH_UNTIL_FLAG = bools
def LED_ear_Flush_Until(ledsProxy, duration=0.05):
	'''
		由全局变量LED_EAR_FLUSH_UNTIL_FLAG控制的ear flush;
		LED_EAR_FLUSH_UNTIL_FLAG为Ture, 一直流水灯;
	'''
	global LED_EAR_FLUSH_UNTIL_FLAG
	while LED_EAR_FLUSH_UNTIL_FLAG == True:
		for i in range(len(RightEarLedList)):
			ledsProxy.fade(LeftEarLedList[i], 1, duration)
			ledsProxy.fade(RightEarLedList[i], 1, duration)
		for i in range(len(RightEarLedList)):
			ledsProxy.fade(LeftEarLedList[i], 0, duration)
			ledsProxy.fade(RightEarLedList[i], 0, duration)
def setFaceFlushFlag(bools):
	global LED_FACE_FLUSH_UNTIL_FLAG
	LED_FACE_FLUSH_UNTIL_FLAG = bools
def LED_face_Flush_Until(ledsProxy, duration=0.05):
	'''
		由全局变量LED_FACE_FLUSH_UNTIL_FLAG控制的ear flush;
		LED_FACE_FLUSH_UNTIL_FLAG为Ture, 一直流水灯;
	'''
	global LED_FACE_FLUSH_UNTIL_FLAG
	while LED_FACE_FLUSH_UNTIL_FLAG == True:
		for index in range(len(FaceLedList)):
			ledsProxy.fade(FaceLedList[index], 1, duration)
		for index in range(len(FaceLedList)):
			ledsProxy.fade(FaceLedList[index], 0, duration)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
