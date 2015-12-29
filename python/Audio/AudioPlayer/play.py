#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < play.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/30 >
#	> Last Changed: 
#	> Description:		AudioPlayer play test
#################################################################

import argparse
from naoqi import ALProxy
import time
import sys

def main(robot_IP, robot_PORT=9559):
	# ----------> Connect to robot <----------
	aup = ALProxy("ALAudioPlayer", robot_IP, robot_PORT)
	# ----------> play music <----------
	try:
		# A single sound file is called using its absolute path
#		fileId = aup.post.playFile("/home/nao/music/Maplestory.mp3")

		# playFile(const std::string& fileName, const float& volume, const float& pan)
		# volume音量[0.0 - 1.0]
		# 声道pan, (-1.0 : left / 1.0 : right / 0.0 : center)
		fileID = aup.post.playFile("/home/nao/music/Maplestory.mp3", 0.5, 1.0) # 重载函数
		print "play music!"
		time.sleep(2)
		
		# 返回现在文件播放的位置（秒数）
		print "Current Position:", aup.getCurrentPosition(fileID)

		# 跳转
		print "Go To 20s"
		aup.goTo(fileID, 20)
		time.sleep(2)
		# 返回文件的长度
		print "file length:", aup.getFileLength(fileID)

		# 返回最大音量
		print "Master Volume:", aup.getMasterVolume()

		# 返回当前文件的音量
		print "Volume:", aup.getVolume(fileID)	

		# 暂停
		aup.pause(fileID)
		print "pause 3 seconds"
		time.sleep(3)
		# 播放
		aup.post.play(fileID)
		print "play again."
		
		time.sleep(60)
		aup.stopAll()
	except KeyboardInterrupt:
		aup.stopAll()
		print ""
		print "Interrupted by user, shutting down"
		sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
