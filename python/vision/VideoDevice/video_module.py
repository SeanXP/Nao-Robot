#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < video_module.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/15 >
#	> Last Changed: 
#	> Description:		VideoSend类, 实现NAO机器人的视频发送功能
#################################################################

import argparse
from naoqi import ALProxy

import Image			# Python Image Library
import random
import socket
import time
import sys
import threading        # 多线程类

class VideoSend(threading.Thread):
	'''
		创建线程类 - VideoSend, 实现NAO机器人的视频发送功能
		run()功能：开启特定端口的服务器，等待连接；客户端连接后，向客户端发送图像数据;
	'''
	def __init__(self, robot_ip, robot_port=9559):
		# 线程类初始化
		threading.Thread.__init__(self)
		self.setDaemon(True)
		# -----------------------------------类成员变量
		# 订阅模块的订阅名称，取消订阅时要用; 
		# 因为调试代码常挂掉程序，没有取消订阅，无法再次订阅相同名称，因此这里加入随机化.
		self.nameID = "video_VM_" + str(random.randint(0,100))
		
		# Camera indexes, 选择摄像头
		self.TopCamera = 0
		self.BottomCamera = 1
		self.XtionCamera = 2			# Xtion Pro Live Depth Camera
		self.cameraIndex = self.TopCamera

		# 分辨率:
		#	kQQVGA (160x120), kQVGA (320x240), kVGA (640x480) or k4VGA (1280x960, only with the HD camera).
		# (Definitions are available in alvisiondefinitions.h)
		RESOLUTION_QQVGA_160 = 0		# 1/4 VGA
		RESOLUTION_QVGA_320 = 1			# 1/2 VGA
		RESOLUTION_VGA_640 = 2			# VGA, 640x480
		self.resolution = RESOLUTION_QQVGA_160
		
		# 文件格式(ColorSpace):
		#	kYuvColorSpace, kYUVColorSpace, kYUV422ColorSpace (9), kRGBColorSpace(11), etc.
		# (Definitions are available in alvisiondefinitions.h)
		ColorSpace_YUV422 = 9	# 0xVVUUYY
		ColorSpace_YUV = 10		# 0xY'Y'VVYY
		ColorSpace_RGB = 11		# 0xBBGGRR
		ColorSpace_BGR = 13		# 0xRRGGBB
		self.colorSpace = ColorSpace_YUV422;

		# 帧率(最高 30 fps):
		self.fps = 30;
		
		self.subscriberID = None
		# 头部摄像头订阅
		self.subscriberID_Top = None
		# 底部摄像头订阅
		self.subscriberID_Bottom = None
		# xtion camera
		self.subscriberID_Xtion = None
		
		# socket 协议, 支持UDP与TCP
		self.protocol = 'UDP'
#		self.protocol = 'TCP'

		# 服务器监听端口
		self.server_ip = robot_ip
		self.listen_port = 8003
		# 开启socket服务器端, 根据self.protocol的协议选择不同的连接方式
		if self.protocol == 'UDP':
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.sock.bind((robot_ip, self.listen_port))
		else: # TCP
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
			self.sock.bind((robot_ip, self.listen_port))
			self.sock.listen(10)
		# 客户端连接标志位
		self.connect_flag = False
		# 发送数据标志位
		self.send_flag = False
		# xtion camera flag, 如果机器人连接Xtion Pro Live, 则调用API:addXtionCamera()设为True;
		# xtion: 支持分辨率QQVGA_160, QVGA_320.
		self.Xtion_flag = False

		# naoqi.ALProxy
		try:
			self.video = ALProxy("ALVideoDevice", robot_ip, robot_port)
		except Exception, e:
			print "class VideoSend::__init__() Could not create proxy by ALProxy"
			print "Error: ", e
			
	def run(self):
		'''
			监听socket连接，连接后持续向客户端发送视频图像;
		'''
		# 1. 订阅相应配置的视频数据
		self.subscribeCamera()
		if self.subscriberID == None:
			self.setCamera(self.TopCamera)
		# 2. 设置发送标志位
		self.send_flag = True
		# 3. 循环发送
		while True: 							# 线程死循环
			if self.send_flag == True:			# 发送数据
				if self.protocol == 'TCP':
					# 等待TCP客户端连接，单线程监听单一客户端
					connection,address = self.sock.accept()
					print '<VideoSend> get TCP client address:', address
					self.connect_flag = True
					while self.connect_flag == True and self.send_flag == True:
						# 发送图像至客户端
						# 1. 获得图像数据
						image = self.video.getImageRemote(self.subscriberID)
						# 2. 发送图像数据
						array = image[6]
						connection.send(array)
					# 断开客户端连接
					connection.close()
					print '<VideoSend> TCP server socket close.'
				else:		# UDP
					# 等待UDP客户端连接, 获得UDP客户端地址; 
					data,address = self.sock.recvfrom(2048) # 直接等待客户端发送UDP数据
					print '<VideoSend> get UDP client address:', address
					self.connect_flag = True
					while self.connect_flag == True and self.send_flag == True:
						# 发送图像至客户端
						# 1. 获得图像数据
						image = self.video.getImageRemote(self.subscriberID)
						# 2. 发送图像数据
						array = image[6]
						self.sock.sendto(array,address)
					print '<VideoSend> UDP server socket close.'
			else:	# 不发送数据, 则延时等待;
				time.sleep(1)
	def stop(self):
		'''停止发送图像数据'''		   
		if self.connect_flag == True:
			# 断开客户端连接
			print '<VideoSend> - close socket connection'
			self.connect_flag = False
		if self.send_flag == True:
			# 停止发送数据
			self.setSendFlag(False)
	def close(self):
		'''关闭类'''
		self.stop()
		time.sleep(1)	# 等待停止
		self.unsubscribeCamera()
	def setSendFlag(self, bools):
		if self.send_flag == False and bools == True:
			# 开始发送视频
			print '<VideoSend> - start send video'
			self.send_flag = bools
		elif self.send_flag == True and bools == False:
			# 停止发送视频
			print '<VideoSend> - stop send video'
			self.send_flag = bools
		else:
			pass
	def addXtionCamera(self):
		self.Xtion_flag = True
	def setCamera(self, index):
		'''设置摄像头'''
		if index == self.TopCamera:
		   print '<VideoSend> - Set Top Camera'
		   self.cameraIndex = self.TopCamera
		   self.subscriberID = self.subscriberID_Top
		elif index == self.BottomCamera:
		   print '<VideoSend> - Set Bottom Camera'
		   self.cameraIndex = self.BottomCamera
		   self.subscriberID = self.subscriberID_Bottom
		elif index == self.XtionCamera and self.Xtion_flag == True:
		   print '<VideoSend> - Set Xtion Camera'
		   self.cameraIndex = self.XtionCamera
		   self.subscriberID = self.subscriberID_Xtion
		else:
		   print 'class VideoSend::setCamera() - Error Camera Index.'
	def switchCamera(self):
		'''切换摄像头'''
		if self.cameraIndex == self.TopCamera:
			self.setCamera(self.BottomCamera)
		elif self.cameraIndex == self.BottomCamera:
			if self.Xtion_flag == True:
				self.setCamera(self.XtionCamera)
			else:
				self.setCamera(self.TopCamera)
		else:
			self.setCamera(self.TopCamera)
	def getCamera(self):
		return self.cameraIndex
	def setResolution(self, resolution):
		pass
	def setColorSpace(self, colorspace):
		pass
	def setFPS(self, fps):
		if fps > 0 and fps <= 30:
			self.fps = fps
		else:
			print 'class VideoSend::setFPS() - Error fps'
	def subscribeCamera(self):
		'''订阅相应参数的视频'''
		# You only have to call the "subscribe" function with those parameters and
		# ALVideoDevice will be in charge of driver initialization and buffer's management.
		# 提前订阅两个, 一个为TopCamera, 一个为BottomCamera, 便于镜头切换;
		self.subscriberID_Top = self.video.subscribeCamera(	self.nameID,
										self.TopCamera,
										self.resolution,
										self.colorSpace,
										self.fps)
		self.subscriberID_Bottom = self.video.subscribeCamera(	self.nameID,
										self.BottomCamera,
										self.resolution,
										self.colorSpace,
										self.fps)
		if self.Xtion_flag == True:
			self.subscriberID_Xtion = self.video.subscribeCamera(	self.nameID,
											self.XtionCamera,
											self.resolution,
											self.colorSpace,
											self.fps)
	def unsubscribeCamera(self):
		# Release image buffer locked by getImageLocal(). 
		# If module had no locked image buffer, does nothing.
		if self.subscriberID_Top != None:
			self.video.releaseImage(self.subscriberID_Top)
			self.video.unsubscribe(self.subscriberID_Top)
			self.subscriberID_Top = None
		if self.subscriberID_Bottom != None:
			self.video.releaseImage(self.subscriberID_Bottom)
			self.video.unsubscribe(self.subscriberID_Bottom)
			self.subscriberID_Bottom = None
		if self.Xtion_flag == True and self.subscriberID_Xtion != None:
			self.video.releaseImage(self.subscriberID_Xtion)
			self.video.unsubscribe(self.subscriberID_Xtion)
			self.subscriberID_Xtion = None
	def getImageRemote(self):
		''' 
			获得一张图像
		'''
		return self.video.getImageRemote(self.subscriberID)
	def getImageInfo(self):
		image = self.video.getImageRemote(self.subscriberID)
		# image : ALImage
		# image[0] : [int] with of the image
		# image[1] : [int] height of the image
		# image[2] : [int] number of layers of the image
		# image[3] : [int] colorspace of the image	
		# image[4] : [int] time stamp in second 
		# image[5] : [int] time stamp in microsecond (and under second)
		# image[6] : [int] data of the image		<<<<<<<<<<<<<<<<<<<<<<<<<<< 默认为YUV422格式
		# image[7] : [int] camera ID
		# image[8] : [float] camera FOV left angle (radian)
		# image[9] : [float] camera FOV top angle (radian)
		# image[10]: [float] camera FOV right angle (radian)
		# image[11]: [float] camera FOV bottom angle (radian)

		# image Info
		print "image.getWidth:", image[0]
		print "image.getHeight:", image[1]
		print "image.getNbLayers:", image[2]
		print "list.length:", len(image)

def main(robot_IP, robot_PORT=9559):
	try:
		video = VideoSend(robot_IP, robot_PORT)
		video.addXtionCamera()
		video.start()
		time.sleep(200)
		video.close()
	except KeyboardInterrupt:
		video.close()
		print "Interrupted by user, shutting down"
		sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
