#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < change_test.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/03/30 >
#	> Last Changed: 
#	> Description:		切换语言包速度测试
#################################################################

import time
from naoqi import ALProxy

robot_ip = "192.168.1.100"
robot_port = 9559	# default port : 9559

tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)

# 根据语言包选择下面其中一条命令。英语语言包不能说汉语，同样汉语语言包不能说英语。
tts.setLanguage("English")

time1 = time.time()
tts.setLanguage("Chinese")
time2 = time.time()
print "English->Chinese:", time2 - time1

time1 = time.time()
tts.setLanguage("English")
time2 = time.time()
print "Chinese->English:", time2 - time1

time1 = time.time()
tts.setLanguage("Chinese")
time2 = time.time()
print "English->Chinese:", time2 - time1

time1 = time.time()
tts.setLanguage("English")
time2 = time.time()
print "Chinese->English:", time2 - time1

# 切换语言包需要较长时间，故尽量不要在程序运行时切换；
# 经过测试，切换汉语包需要2秒，切换英语包需要0.8秒；
# 另外，下载的英语包为一百多兆，而汉语包只有十兆；尽量使用英语包；
# English->Chinese: 2.00102996826
# Chinese->English: 0.818722009659
