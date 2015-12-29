#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < server.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/23 >
#	> Last Changed: 
#	> Description:		远程控制-客户端
#						向服务器发送指令，查看服务器回执消息。
#################################################################

#! /usr/bin/env python

import argparse
from naoqi import ALProxy
import socket
import time

LISTEN_PORT = 8001 # 服务器监听端口

# command 
COMMAND_DISCONNECT = 'DISCONNECT'
COMMAND_HEADYAW = 'HEADYAW'     # 头左右
COMMAND_HEADPITCH = 'HEADPITCH' # 头上下

# flag
CONNECT = False

def main(robot_IP, robot_PORT=9559):
	# ----------> 连接socket服务器监听端口 <----------
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((robot_IP, LISTEN_PORT))
	time.sleep(2)

	CONNECT = True
	while CONNECT == True: 
		# 输入指令
		command = raw_input("Command code:")
		# socket 发送指令
		sock.send(command)
		if command == COMMAND_HEADYAW or command == COMMAND_HEADPITCH:
	   		value = raw_input("Value:")
			sock.send(value)

		# socket 接受返回消息
		buf = sock.recv(1024)
		print buf
		if command == COMMAND_DISCONNECT: 
			CONNECT = False
	sock.close() # 与服务器端断开socket连接

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
