#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < PhotoCapture.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/01 >
#	> Last Changed: 
#	> Description:		使用机器人拍摄图片，并保存为图片文件
#################################################################

import argparse
import sys
import time
from naoqi import ALProxy

def main(robot_IP, robot_PORT=9559):
	# ----------> Connect to robot <----------
	try:
		photoCapture = ALProxy("ALPhotoCapture", robot_IP, robot_PORT)
	except Exception, e:
		print "Error when creating ALPhotoCapture proxy:"
		print e
		exit(1)
	
	# ----------> Photo Capture<----------
	# Take 3 pictures in VGA and store them in robot: '/home/nao/recordings/cameras/'

	# 设置分辨率，{ 0 = kQQVGA(160*120), 1 = kQVGA(320*240), 2 = kVGA(640*480) }
	photoCapture.setResolution(0)
	# 设置图片格式，bmp, dib, jpeg, jpg 等等
	photoCapture.setPictureFormat("jpg")
	time_start = time.time()
	photoCapture.takePictures(10, "/home/nao/recordings/cameras/", "image")
	time_end = time.time()
	print 'cost time:', time_end - time_start # 默认200ms间隔，拍摄10张需要2秒

	# This call returns ['/home/nao/recordings/cameras/image_0.jpg', 
	#					'/home/nao/recordings/cameras/image_1.jpg', 
	#					'/home/nao/recordings/cameras/image_2.jpg']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
