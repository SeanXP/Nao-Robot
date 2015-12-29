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
import socket
import random
from naoqi import ALProxy

LISTEN_PORT = 8003 		# 服务器监听端口

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
#	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		# SOCK_STREAM, TCP协议
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)			# SOCK_DGRAM, UDP协议
	sock.bind((IP, LISTEN_PORT))
#	sock.listen(10)			# UDP不需要连接

	naoImage = camProxy.getImageRemote(videoClient)
	array = naoImage[6]
	print 'image data length:', len(array) 
	print '---------------------------------------------'

	global connection
	try:
		print 'Waiting for UDP data'
		data,address = sock.recvfrom(2048)			# 直接等待客户端发送UDP数据
		print 'get UDP data:', data
		print 'address', address
		while True: 		# 等待客户端连接，单线程监听单一客户端
#			connection,address = sock.accept()			# UDP没有TCP这样的连接过程;
			# 发送YUV422图像至UDP客户端
			naoImage = camProxy.getImageRemote(videoClient)
			array = naoImage[6]	
			sock.sendto(array,address)
			print 'send date successful.'
		sock.close()
		print 'socket close.'
	except KeyboardInterrupt: # CTRL+C, 关闭服务器端程序;
		print ""
		print "Interrupted by user, shutting down"
		camProxy.unsubscribe(videoClient)
		print 'unsubscribe nao video device'
		sock.close()
		print 'socket close.'
		sys.exit(0)

if __name__ == '__main__':
	IP = "192.168.2.100"  # Replace here with your NaoQi's IP address.
	PORT = 9559

  	# Read IP address from first argument if any.
  	if len(sys.argv) > 1:
		IP = sys.argv[1]

	main(IP, PORT)
