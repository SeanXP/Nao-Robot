#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < video_image.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/22 >
#	> Last Changed: 
#	> Description:		设计基于Nao机器人ALVideoDevice模块的VideoImage类, 实现一些常用的功能;	
#################################################################
import argparse
from naoqi import ALProxy

import Image			# Python Image Library
import random
import time
import sys
import threading        # 多线程类

class VideoImage(threading.Thread):
	'''
		创建线程类 - VideoImage, 实现NAO机器人的图像功能;
	'''
	def __init__(self, robot_ip, robot_port=9559):
		# 线程类初始化
		threading.Thread.__init__(self)
		self.setDaemon(True)
		# -----------------------------------类成员变量
		# 订阅模块的订阅名称，取消订阅时要用; 
		# 因为调试代码常挂掉程序，没有取消订阅，无法再次订阅相同名称，因此这里加入随机化.
		self.nameID = "video_image_" + str(random.randint(0,100))
		
		# Camera indexes, 选择摄像头
		self.TopCamera = 0
		self.BottomCamera = 1
		self.XtionCamera = 2			# Xtion Pro Live Depth Camera
		self.cameraIndex = self.TopCamera

		# 分辨率:
		#	kQQVGA (160x120), kQVGA (320x240), kVGA (640x480) or k4VGA (1280x960, only with the HD camera).
		# (Definitions are available in alvisiondefinitions.h)
		self.RESOLUTION_QQVGA_160 = 0		# 1/4 VGA
		self.RESOLUTION_QVGA_320 = 1			# 1/2 VGA
		self.RESOLUTION_VGA_640 = 2			# VGA, 640x480
		self.resolution = self.RESOLUTION_QVGA_320
		
		# 文件格式(ColorSpace):
		#	kYuvColorSpace, kYUVColorSpace, kYUV422ColorSpace (9), kRGBColorSpace(11), etc.
		# (Definitions are available in alvisiondefinitions.h)
		ColorSpace_YUV422 = 9	# 0xVVUUYY
		ColorSpace_YUV = 10		# 0xY'Y'VVYY
		ColorSpace_RGB = 11		# 0xBBGGRR
		ColorSpace_BGR = 13		# 0xRRGGBB
		self.colorSpace = ColorSpace_RGB;

		# 帧率(最高 30 fps):
		self.fps = 30;
		
		self.subscriberID = None
		# 头部摄像头订阅
		self.subscriberID_Top = None
		# 底部摄像头订阅
		self.subscriberID_Bottom = None
		# xtion camera
		self.subscriberID_Xtion = None
		
		# xtion camera flag, 如果机器人连接Xtion Pro Live, 则调用API:addXtionCamera()设为True;
		# xtion: 支持分辨率QQVGA_160, QVGA_320.
		self.Xtion_flag = False

		# 保存图片后是否直接使用PIL打开图片
		self.show_flag = False

		# naoqi.ALProxy
		try:
			self.video = ALProxy("ALVideoDevice", robot_ip, robot_port)
		except Exception, e:
			print "class VideoImage::__init__() Could not create proxy by ALProxy"
			print "Error: ", e
			
	def run(self):
		pass
	def stop(self):
		pass
	def close(self):
		'''关闭类'''
		self.stop()
		time.sleep(1)	# 等待停止
		self.unsubscribeCamera()
	def addXtionCamera(self):
		self.Xtion_flag = True
	def setCamera(self, index):
		'''设置摄像头'''
		if index == self.TopCamera:
		   print '<VideoImage> - Set Top Camera'
		   self.cameraIndex = self.TopCamera
		   self.subscriberID = self.subscriberID_Top
		elif index == self.BottomCamera:
		   print '<VideoImage> - Set Bottom Camera'
		   self.cameraIndex = self.BottomCamera
		   self.subscriberID = self.subscriberID_Bottom
		elif index == self.XtionCamera and self.Xtion_flag == True:
		   print '<VideoImage> - Set Xtion Camera'
		   self.cameraIndex = self.XtionCamera
		   self.subscriberID = self.subscriberID_Xtion
		else:
		   print 'class VideoImage::setCamera() - Error Camera Index.'
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
		'''
			设置分辨率
			此函数必须在self.subscribeCamera()之前调用才有效;
		'''

		if resolution == 320:
			self.resolution = self.RESOLUTION_QVGA_320
		elif resolution == 160:
			self.resolution = self.RESOLUTION_QQVGA_160	
		elif resolution == 640:
			self.resolution = self.RESOLUTION_VGA_640
		else:
			pass
	def setColorSpace(self, colorspace):
		pass
	def setFPS(self, fps):
		if fps > 0 and fps <= 30:
			self.fps = fps
		else:
			print 'class VideoImage::setFPS() - Error fps'
	def setShowFlag(self, bools):
		self.show_flag = bools
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
		# image[0] : [int] width of the image
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
		print "width of the image:		", image[0]
		print "height of the image:		", image[1]
		print "image.getNbLayers:		", image[2]
		print 'colorspace of the image:	', image[3]
		print 'time stamp (second):		', image[4]
		print 'time stamp (microsecond):', image[5]
		print 'data of the image (ignore to print). - image[6]', len(image[6])
		print 'camera ID:				', image[7]	
		print 'camera FOV left angle:	', image[8]
		print 'camera FOV top angle:	', image[9]
		print 'camera FOV right angle:	', image[10]
		print 'camera FOV bottom angle:	', image[11]
		
		self.saveImage(image[6], image[0], image[1], 'RGB', 'PNG', 'camImage.png')	   
	def saveImage(self, image_data, image_width, image_height, 
			image_colorspace='RGB', image_format='PNG', image_filename='camImage.png'):
		# use Python Image Library (PIL)
		# Create a PIL Image from our pixel array.
		image = Image.fromstring(image_colorspace, (image_width, image_height), image_data)
		# Save the image.
		print '<VideoImage> - save image to', image_filename
		image.save(image_filename, image_format)
		if self.show_flag == True:
			image.show()
	def takeImage(self, number):
		for num in range(number):
			naoImage = self.video.getImageRemote(self.subscriberID)
			self.saveImage(naoImage[6], naoImage[0], naoImage[1], 'RGB', 'PNG', 'camImage'+str(num)+'.png')
	def takeRGBDimage(self, number, delay=0):
		'''
			number: the number of image
			delay: delay time of taking image
		'''
		# rgb image: top camera
		# depth image: Xtion camera
		for num	in range(number):
			rgbImage = self.video.getImageRemote(self.subscriberID_Top)
			depthImage = self.video.getImageRemote(self.subscriberID_Xtion)
			self.saveImage(rgbImage[6], rgbImage[0], rgbImage[1], 'RGB', 'PNG', 'rgbImage_'+str(num)+'.png')
			self.saveImage(depthImage[6], depthImage[0], depthImage[1], 'RGB', 'PNG', 'depthImage_'+str(num)+'.png')
			if delay != 0:
				time.sleep(delay)
	def cameraSpeedTest(self, cameraIndex=0):
		'''Test Camera Speed'''
		if cameraIndex == self.TopCamera:
			self.setCamera(cameraIndex)
			cameraName = 'TopCamera'
		elif cameraIndex == self.BottomCamera:
			self.setCamera(cameraIndex)
			cameraName = 'BottomCamera'
		elif cameraIndex == self.XtionCamera: 
			if self.Xtion_flag == True:
				self.setCamera(cameraIndex)			
				cameraName = 'XtionCamera'
			else:
				print 'Xtion Flag:', self.Xtion_flag
				return None
		else:
			print 'VideoImage::cameraSpeedTest() - Error cameraIndex:', cameraIndex
			return None
		number = 100
		time_sum = 0
		for num in range(number):	
			t0 = time.time()
			naoImage = self.video.getImageRemote(self.subscriberID)
			t1 = time.time()
			print cameraName, 'acquisition delay', t1 - t0
			time_sum += t1 - t0
		print cameraName, '- time cost:', time_sum
		print cameraName, '- average:', time_sum / number
		print '--------------------------------------------------'

def main(robot_IP, robot_PORT=9559):
	try:
		video = VideoImage(robot_IP, robot_PORT)
#		video.addXtionCamera()
#		video.setResolution(160)
		video.subscribeCamera()	
		video.setCamera(0)		# top camera
#		video.setCamera(1)		# bottom camera
#		video.setCamera(2)		# xtion camera (optional)
		video.getImageInfo()
		
#		video.takeImage(20)
#		video.takeRGBDimage(2000)

#		video.cameraSpeedTest(0)	
#		video.cameraSpeedTest(1)	
#		video.cameraSpeedTest(2)	
#		video.start()
#		time.sleep(200)
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
