#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < check_camera.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/05/04 >
#	> Last Changed: 
#	> Description:	
#################################################################

import argparse
from naoqi import ALProxy

def main(robot_IP, robot_PORT=9559):
	# ----------> Connect to robot <----------
	video = ALProxy("ALVideoDevice", robot_IP, robot_PORT)
	# ----------> <----------
	# Gets list of available camera indexes.
	print 'getCameraIndexes():', video.getCameraIndexes()
	# return [0,1] or [0,1,2]. Xtion Pro Live
	
	for num in video.getCameraIndexes():
		print '------------------'
		print 'Camera Index:', num
		print 'Camera Name:', video.getCameraName(num)
		print 'Camera Model:', video.getCameraModel(num)
		print 'Camera Frame Rate:', video.getFrameRate(num)
		print 'Camera Resolution:', video.getResolution(num)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
