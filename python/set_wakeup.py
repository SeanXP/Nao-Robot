#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < set_wakeup.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/18 >
#	> Last Changed: 
#	> Description:		Wake up rebot.
#################################################################

import argparse
from naoqi import ALProxy

def main(robot_IP, robot_PORT=9559):
	# ----------> Connect to robot <----------
	motion = ALProxy("ALMotion", robot_IP, robot_PORT)
	# ----------> <----------
	motion.wakeUp()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.2.100", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
	# ----------> 执行main函数 <----------
    main(args.ip, args.port)
