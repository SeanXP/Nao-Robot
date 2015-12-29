#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < set_English.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/30 >
#	> Last Changed: 
#	> Description:
#################################################################

from naoqi import ALProxy

robot_ip = "192.168.1.100"
robot_port = 9559	# default port : 9559

tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)

tts.setLanguage("English")
tts.say("Hello, world! I am Nao robot!")

# 切换语言包需要较长时间，故尽量不要在程序运行时切换；
