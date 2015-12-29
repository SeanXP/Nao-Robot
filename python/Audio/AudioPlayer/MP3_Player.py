#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < MP3_Player.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/13 >
#	> Last Changed: 
#	> Description:		Class MP3player
#################################################################

'''
	基于Nao robot实现一个MP3播放器
'''

from naoqi import ALProxy
import argparse
import sys
import os
import time
import threading        # 多线程类
import urllib   		# urllib.urlretrieve

class MP3player(threading.Thread):
	'''
		创建线程类 - MP3player, 实现Nao机器人播放音乐
	'''
	def __init__(self, robot_ip, robot_port=9559):
		# 线程类初始化
		threading.Thread.__init__(self)
		# 类成员变量
		self.path = '/home/nao/music/'	# 音乐文件夹路径
		self.playlist = []      	# 歌曲播放列表；程序启动后会扫描一遍音乐文件夹；为绝对路径地址
		self.playindex = 0      	# 指向当前播放音乐的索引, 范围 range(len(MusicList))
		self.playflag = False    	# 播放标志位, 播放音乐时标识为True
		self.playfileID = None   	# 正在播放文件的fileID
		self.volume = 0.50     		# 音量, [0.0 ~ 1.0]

		# naoqi.ALProxy
		try:
			self.aup = ALProxy("ALAudioPlayer", robot_ip, robot_port)
		except Exception, e:
			print ""
			print "class MP3player::__init__() : Could not create proxy by ALProxy"
			print "Error: ", e

		# 1. 扫描音乐文件夹，生成播放列表
		self.scanMP3()	
		# 2. 载入第一首音乐文件
		if len(self.playlist) != 0:	# 至少有一首歌曲
			self.playfileID = self.aup.loadFile(self.playlist[self.playindex])
		else: # 一首歌曲也没有
			print 'class MP3player::__init__() : find: .mp3: No such file or directory'
		# 3. 等待start; 即在外部调用start()函数，会执行类函数run();
   		#	start()函数只执行一次;
		#	start()函数中有一段死循环，用于检测播放进度以便于结束时切换下一首歌曲;
		# 将该线程设置为守护线程，这样就主线程就不会以为该线程的循环未结束而挂起。
		self.setDaemon(True)
		self.start()			# run()函数仅为一段死循环，作为进度检测之用;

	def getPath(self):
		return self.path
	def getPlayList(self):
		return self.playlist
	def getPlayIndex(self):
		return self.playindex
	def getFlag(self):
		return self.playflag
	def getFileID(self):
		return self.playfileID
	def getVolume(self):
		return self.volume
	
	def setPath(self, path):
		'''检测路径是否存在，存在则可以配置 '''
		if os.path.exists(path) == True:
			self.path = path
		else:
			print 'class MP3player::setPath() Error: Wrong music path :', path
	def setVolume(self, volume=0.5):
		'''音量调节, volume [0,1]'''
		if volume >= 0 and volume <= 1:
		   self.volume = volume
		   self.aup.setVolume(self.playfileID, self.volume)
		   print '<Music Volume>:', self.volume * 100, '%'
		else:
			print 'class MP3player::setVolume() Error: wrong volume'
	def upVolume(self, change=0.05):
		'''
			增大音量，每次增量change默认为0.05
			无法增大则直接返回
		'''
		volume = self.volume + change
		if volume <= 1:
			self.aup.setVolume(self.playfileID, volume)	
		else:
			pass
	def downVolume(self, change=0.05):
		volume = self.volume - change
		if volume >= 0:
			self.aup.setVolume(self.playfileID, volume)
		else:
			pass
	def nextSong(self):	
		self.playindex = (self.playindex + 1) % len(self.playlist)
		print '<Music Next Song>:', self.playlist[self.playindex]
		if self.playflag == False:	# 暂停状态下的下一首, 仅载入音乐
			self.playfileID = self.aup.loadFile(self.playlist[self.playindex])
		else:						# 播放状态下的下一首, 暂停, 切换下一首音乐
			self.pause()
			self.playfileID = self.aup.loadFile(self.playlist[self.playindex])	
			self.play()
	def previousSong(self):
		self.playindex = (self.playindex + len(self.playlist) - 1) % len(self.playlist)
		print '<Music Previous Song>:', self.playlist[self.playindex]
		if self.playflag == False:	# 暂停状态下的上一首, 仅载入音乐
			self.playfileID = self.aup.loadFile(self.playlist[self.playindex])
		else:						# 播放状态下的上一首, 暂停, 切换上一首音乐
			self.pause()
			self.playfileID = self.aup.loadFile(self.playlist[self.playindex])	
			self.play()
	def run(self):
		'''调用类函数start(), 会运行该函数; start()只能调用一次'''
		# 开启进度检测
		while True:
			if self.playflag == True: # 正在播放音乐
				postion = self.aup.getCurrentPosition(self.playfileID)
				length = self.aup.getFileLength(self.playfileID)
				if postion >= length - 2: # 播放进度即将结束，此时直接切换下一首歌曲
					self.nextSong()
			# 1秒检测一次进度
			time.sleep(1)

	def play(self):
		self.setFlag(True)
	def stop(self):
		self.setFlag(False)
	def pause(self):
		self.setFlag(False)
	def setFlag(self, flag):
		'''根据标志位的切换，执行不同的操作
			False -> True, 播放音乐; 默认已载入音乐;
			True -> False, 停止音乐;
		'''
		if self.playflag == False and flag == True:
			# 播放音乐
			print '<Music Play>'
			self.playflag = flag
			self.aup.post.playInLoop(self.playfileID, self.volume, 0)
		elif self.playflag == True and flag == False:
			# 停止音乐
			print '<Music Pause>'
			self.playflag = flag
			self.aup.pause(self.playfileID)
		else:
			pass
	def forward(self, seconds=10):
		'''快进歌曲, 参数seconds表示快进的秒数，默认10s'''
		# 获得当前播放位置
		position = self.aup.getCurrentPosition(self.playfileID)
		# 判断是否可以快进
		if position + seconds < self.aup.getFileLength(self.playfileID):	
			# 可以快进
			self.aup.goTo(self.playfileID, position + seconds)
			print "Music Position >> ", self.aup.getCurrentPosition(self.playfileID)
		else:
			# 快进到歌曲结束，直接下一首
			self.nextSong()
	def rewind(self, seconds=10):
		'''快退歌曲, 参数seconds表示快退的秒数，默认10s'''
		# 获得当前播放位置
		position = self.aup.getCurrentPosition(self.playfileID)
		# 判断是否可以快退
		if position - seconds >= 0:	
			# 可以快退
			self.aup.goTo(self.playfileID, position - seconds)
		else:
			# 重新播放歌曲
			self.aup.goTo(self.playfileID, 0)
		print "Music Position << ", self.aup.getCurrentPosition(self.playfileID)

	def scanMP3(self):
		'''在音乐文件夹中寻找mp3格式的音乐，加入播放列表'''
		for root, dirs, files in os.walk(self.path):
			# root   #当前遍历到的目录的根
			# dirs   #当前遍历到的目录的根下的所有目录
			# files  #当前遍历到的目录的根下的所有文件
			for filename in files:
				if filename.find('.mp3') != -1:			# 找不到后缀才返回-1
					filepath = os.path.join(root, filename)
					self.playlist.append(filepath)		# 将找到的mp3文件的相对路径加入播放列表
	def downloadMP3(self, name, url):
		'''
			下载MP3音乐, 下载好音乐后自动切歌
			参数:	name, 下载音乐的名称;
					url, 下载地址;
		'''
		try:
			# 使用urllib下载音乐
			print "<Music Download> Name:", name
			print "<Music Download> URL: ", url
			urllib.urlretrieve(url, self.path + name + '.mp3')
			print '<Music Download> Status: Download Completed!'
			# 将下载好的音乐添加在播放列表中
			self.playlist.append(self.path + name + '.mp3')
			# 切换音乐
			self.playindex = len(self.playlist) - 2
			self.nextSong()
			if self.playflag == False:	# 没有播放音乐, 则开始播放
				self.play()
		except Exception,e:
		   print 'Exception:',e
		   print 'class MP3player::downloadMP3()'


def main(robot_IP, robot_PORT=9559):
	# ----------> avoidance <----------
	player = MP3player(robot_IP, robot_PORT)
	try:
		print 'test play()'
		player.play()	
		time.sleep(2)
		
		print 'test pause()'
		player.pause()
		time.sleep(2)
		
		print 'test play()'
#		player.setFlag(True)
		player.play()
		time.sleep(2)

		print 'test next song'
		player.nextSong()	
		time.sleep(2)

		print 'test previous song'
		player.previousSong()
		player.previousSong()
		player.previousSong()
		time.sleep(2)

		print 'test forward'
		player.forward()
		time.sleep(2)

		print 'test rewind'
		player.rewind()
		time.sleep(2)

		print 'test forward'
		player.forward()
		time.sleep(2)

#		print 'test download'
		music_name = '漫步人生路'
		url = 'http://m1.music.126.net/YoKvhEpzjqFq79vy2jApLg==/1018147767327618.mp3'
		player.downloadMP3(music_name, url)

#		print 'test stop'
#		player.stop()
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		# 中断程序
		player.stop()			# 1. 调用类函数stop()停止
#		player.setFlag(False)	# 2. 调用类函数setFlag()配置PlayFlag为False从而停止音乐播放。
		print "Interrupted by user, shutting down"
		sys.exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
	parser.add_argument("--port", type=int, default=9559, help="Robot port number")
	args = parser.parse_args()
	# ----------> 执行main函数 <----------
	main(args.ip, args.port)
