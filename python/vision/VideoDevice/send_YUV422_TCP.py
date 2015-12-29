#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < send_YUV422.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/13 >
#	> Last Changed: 
#	> Description:		send YUV422 image file to socket client.
#################################################################

import sys
import time

import Image		# Python Image Library
import socket
import random
import struct

from naoqi import ALProxy

LISTEN_PORT = 8003 		# 服务器监听端口
CONNECT = False         # 客户端连接Flag
connection = None

def main(IP, PORT):
	camProxy = ALProxy("ALVideoDevice", IP, PORT)
#	resolution = 2    # VGA 640x480
	resolution = 0    # kQQVGA, 160x120
#	colorSpace = 11   # RGB
#	colorSpace = 10   # YUV
	colorSpace = 9    # YUV422

	# 程序测试经常挂掉，导致subscriberID未被取消订阅，需要更换订阅号；这里加入随机;
	subscriberID = 'send_YUV422_' + str(random.randint(0,100))

	videoClient = camProxy.subscribe(subscriberID, resolution, colorSpace, 30)

	# ----------> 开启socket服务器监听端口 <----------
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((IP, LISTEN_PORT))
	sock.listen(10)

	naoImage = camProxy.getImageRemote(videoClient)
	array = naoImage[6]
#	print 'VIDEO#' + array + '\r'
	print 'image data length:', len(array) 
	print 'print test over.'
	print '---------------------------------------------'

	global connection
	try:
		while True: 		# 等待客户端连接，单线程监听单一客户端
			print 'Waiting for a connection'
			connection,address = sock.accept()
			print 'socket client connected.'
			CONNECT = True
			while CONNECT == True:
				# 发送YUV422图像至客户端
				naoImage = camProxy.getImageRemote(videoClient)
				array = naoImage[6]	

#				for i in range(len(array)):
#					connection.send(array[i])
#					if (i % 5 == 0):
#						connection.send('\r')
#				connection.send('\r')

				connection.send(bytes(array+'\n', 'utf-8'))

#				connection.send('VIDEO#' + array + '\r#OVER\r')
				print 'send image date successful.'
#				time.sleep(1)	
				CONNECT = False
			print 'socket client disconnect.'
	except KeyboardInterrupt: # CTRL+C, 关闭服务器端程序;
		print ""
		print "Interrupted by user, shutting down"
		camProxy.unsubscribe(videoClient)
		print 'unsubscribe nao video device'
		if connection != None:
			connection.close()	
			print 'socket connection closed.'
		sys.exit(0)


#		imageWidth = naoImage[0]
#  		imageHeight = naoImage[1]
#  		array = naoImage[6]

		#im = Image.fromstring("YUV", (imageWidth, imageHeight), array)
		#im.save("camImage.png", "PNG")
		#im.show()

if __name__ == '__main__':
	IP = "192.168.2.100"  # Replace here with your NaoQi's IP address.
	PORT = 9559

  	# Read IP address from first argument if any.
  	if len(sys.argv) > 1:
		IP = sys.argv[1]

	main(IP, PORT)
