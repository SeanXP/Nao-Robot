#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < touch_mp3player.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/30 >
#	> Last Changed: 
#	> Description:		基于Nao robot实现一个MP3播放器
#						头部front: 		下一首
#						头部middle:		播放/暂停
#						头部near:		上一首
#						右脚:			volume -
#						左脚:			volume +
#						左手left(外侧):	快进
#						右手right(外侧):快退
#################################################################
"""
	Nao Robot Mp3 player, 用于机器人音频编程练习；
	指定音乐文件夹后，程序会自动扫描内部所有的mp3文件；
	注：由于机器人没有提供检测歌曲结束的API，这里开一线程，监听播放position, 到结束后触发next song;
"""
import argparse
import sys
import time
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import os
import thread

# 歌曲文件夹
MusicPath = '/home/nao/music/'
MusicList = []		# 歌曲列表；程序启动后会扫描一遍音乐文件夹；为绝对路径地址 
MusicPoint = 0		# 指向当前播放音乐的索引, 范围 range(len(MusicList))
PlayFlag = False 	# 播放标志位, 播放音乐时标识为True
PlayFileID = None	# 正在播放文件的fileID
MyVolume = 0.50		# 音量, [0.0 ~ 1.0]

# Global variable to store the FrontTouch module instance
FrontTouch = None			# 下一首
MiddleTouch = None			# 开始/暂停
RearTouch = None			# 上一首
LeftFootTouch = None		# Volume +
RightFootTouch = None		# Volume -
LeftHandLeftTouch = None	# 快进
RightHandRightTouch = None	# 快退

tts = None
memory = None
aup = None
leds = None

class FrontTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
        # Subscribe to FrontTactilTouched event:
		memory.subscribeToEvent("FrontTactilTouched",
			"FrontTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		# value == 0, 为松开触摸区域事件，这里直接忽略；
		if value == 0:
			return
		# Unsubscribe to the event when talking,
		# to avoid repetitions
		memory.unsubscribeToEvent("FrontTactilTouched",
			"FrontTouch")

		global MusicPoint, PlayFileID
		MusicPoint = (MusicPoint + 1) % len(MusicList)
		filename = MusicList[MusicPoint]
		print "next song:", MusicList[MusicPoint]
		if PlayFlag == True:		# 播放音乐时切歌
			# 停止播放
			aup.pause(PlayFileID)
			# 切歌播放
			PlayFileID = aup.post.playFileInLoop(filename, MyVolume, 0)
		else:						# 暂停音乐时切歌
			# 载入下一首歌曲
			PlayFileID = aup.loadFile(filename)
			
        # Subscribe again to the event
		memory.subscribeToEvent("FrontTactilTouched",
			"FrontTouch",
			"onTouched")


class MiddleTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("MiddleTactilTouched",
			"MiddleTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		if value == 0:
			return
		memory.unsubscribeToEvent("MiddleTactilTouched",
			"MiddleTouch")
		
		global PlayFlag, PlayFileID
		if PlayFlag == False:			# 没有播放音乐，则开始播放音乐
			PlayFlag = True
			aup.post.playInLoop(PlayFileID, MyVolume, 0)
			print "Play"
		else:							# 正在播放音乐，则暂停播放
			PlayFlag = False
			aup.pause(PlayFileID)
			print "Pause"

		memory.subscribeToEvent("MiddleTactilTouched",
			"MiddleTouch",
			"onTouched")

class RearTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("RearTactilTouched",
			"RearTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		if value == 0:
			return
		memory.unsubscribeToEvent("RearTactilTouched",
			"RearTouch")

		global MusicPoint, PlayFileID
		MusicPoint = (MusicPoint + len(MusicList) - 1) % len(MusicList)
		filename = MusicList[MusicPoint]
		print "Previous Song:", MusicList[MusicPoint]
		if PlayFlag == True:		# 播放音乐时切歌
			# 停止播放
			aup.pause(PlayFileID)
			# 切歌播放
			PlayFileID = aup.post.playFileInLoop(filename, MyVolume, 0)
		else:						# 暂停音乐时切歌
			# 载入下一首歌曲
			PlayFileID = aup.loadFile(filename)

		memory.subscribeToEvent("RearTactilTouched",
			"RearTouch",
			"onTouched")

class LeftFootTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("LeftBumperPressed",
			"LeftFootTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		if value == 0:
			return
		memory.unsubscribeToEvent("LeftBumperPressed",
			"LeftFootTouch")
		global MyVolume, PlayFileID
		if  MyVolume < 1.00:
			MyVolume = MyVolume + 0.05	
			aup.setVolume(PlayFileID, MyVolume)
		print "Volume:", aup.getVolume(PlayFileID)
		memory.subscribeToEvent("LeftBumperPressed",
			"LeftFootTouch",
			"onTouched")

class RightFootTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("RightBumperPressed",
			"RightFootTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		if value == 0:
			return
		memory.unsubscribeToEvent("RightBumperPressed",
			"RightFootTouch")

		global MyVolume, PlayFileID
		if MyVolume > 0:
			MyVolume = MyVolume - 0.05	
			aup.setVolume(PlayFileID, MyVolume)
		print "Volume:", aup.getVolume(PlayFileID)

		memory.subscribeToEvent("RightBumperPressed",
			"RightFootTouch",
			"onTouched")

class LeftHandLeftTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("HandLeftLeftTouched",
			"LeftHandLeftTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		if value == 0:
			return
		memory.unsubscribeToEvent("HandLeftLeftTouched",
			"LeftHandLeftTouch")
		position = aup.getCurrentPosition(PlayFileID)	
		if position + 10 < aup.getFileLength(PlayFileID):
			aup.goTo(PlayFileID, position + 10)
			print "Position >>:", aup.getCurrentPosition(PlayFileID)
		memory.subscribeToEvent("HandLeftLeftTouched",
			"LeftHandLeftTouch",
			"onTouched")

class RightHandRightTouch(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		memory.subscribeToEvent("HandRightRightTouched",
			"RightHandRightTouch",
			"onTouched")

	def onTouched(self, strVarName, value):
		if value == 0:
			return
		memory.unsubscribeToEvent("HandRightRightTouched",
			"RightHandRightTouch")
		position = aup.getCurrentPosition(PlayFileID)	
		if position - 10 >= 0:
			aup.goTo(PlayFileID, position - 10)
			print "Position <<:", aup.getCurrentPosition(PlayFileID)
		memory.subscribeToEvent("HandRightRightTouched",
			"RightHandRightTouch",
			"onTouched")

def main(ip, port):
	# We need this broker to be able to construct
	# NAOqi modules and subscribe to other modules
	# The broker must stay alive until the program exists
	
	myBroker = ALBroker("myBroker",
		"0.0.0.0",   # listen to anyone
		0,           # find a free port and use it
		ip,          # parent broker IP
		port)        # parent broker port

	global tts, memory, aup, leds
	tts = ALProxy("ALTextToSpeech", ip, port)
	memory = ALProxy("ALMemory", ip, port)
	leds = ALProxy("ALLeds", ip, port)
	aup = ALProxy("ALAudioPlayer", ip, port)

	# 启动后需要提前加载第一个音乐文件
	global PlayFileID
	scan_mp3()			# 先扫描文件夹
	filename = MusicList[MusicPoint]
	PlayFileID = aup.loadFile(filename)

	global FrontTouch, MiddleTouch, RearTouch
	global LeftFootTouch, RightFootTouch
	global LeftHandLeftTouch, RightHandRightTouch
	FrontTouch = FrontTouch("FrontTouch")
	MiddleTouch = MiddleTouch("MiddleTouch")
	RearTouch = RearTouch("RearTouch")
	LeftFootTouch = LeftFootTouch("LeftFootTouch")
	RightFootTouch = RightFootTouch("RightFootTouch")
	LeftHandLeftTouch = LeftHandLeftTouch("LeftHandLeftTouch")
	RightHandRightTouch = RightHandRightTouch("RightHandRightTouch")

	# 创建一个线程，监听播放进度, 实现播放歌曲结束后自动切换下一首歌曲;
	thread.start_new_thread(timer, ())

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print
		print "Interrupted by user, shutting down"
		aup.stopAll()
		print "Stop All Music"
		myBroker.shutdown()
		sys.exit(0)

def scan_mp3():
	'''
		从指定的文件夹中扫描出MP3格式的文件
	'''
	global MusicList
	for root, dirs, files in os.walk(MusicPath):
    	# root   #当前遍历到的目录的根
    	# dirs   #当前遍历到的目录的根下的所有目录
    	# files  #当前遍历到的目录的根下的所有文件
		for filename in files:
			if filename.find('.mp3') != -1:	 		# 找不到后缀才返回-1
				filepath = os.path.join(root, filename)
				MusicList.append(filepath)			# 将找到的mp3文件的地址加入MusicList	

def timer():
	'''
		检查当前音乐的播放进度，结束后切换下一首歌曲;
	'''
	while True:
		postion = aup.getCurrentPosition(PlayFileID)	
		length = aup.getFileLength(PlayFileID)
		if PlayFlag == True and postion == length - 2: # 正在播放，且进度即将结束
			memory.raiseEvent('FrontTactilTouched', 1.0) # 触发下一首对应的事件
		time.sleep(1)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default="127.0.0.1",
						help="Robot ip address")
	parser.add_argument("--port", type=int, default=9559,
						help="Robot port number")
	args = parser.parse_args()
	main(args.ip, args.port)
