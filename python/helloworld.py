#! /usr/bin/env python
#-*- coding: utf-8 -*-
from naoqi import ALProxy
#必须要加上面一行代码，表示使用utf-8编码格式，否则python解释器不能识别汉字编码，运行将出现句法错误

# Python SDK key concepts
# 1. Import ALProxy
# 2. Create an ALproxy to the module you want to use
# 3. Call a method

robot_ip = "192.168.2.100"
robot_port = 9559	# default port : 9559

# ALTextToSpeech is the module of NAoqi dedicated to speech. 
# The say method makes the robot pronounce the string given in parameter.

# tts is the name we gave to the object instance(could have been myspeechmodule or speakingmodule).
# ALProxy() is a class of objects, allowing you to have acces to all the methods of a module.
# ALTextToSpeech is the name of the module of NAOqi we want to use.
# IP and Port (9559) of the robot are also specified (it was not the case with Choregraphe).
tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)

# 根据语言包选择下面其中一条命令。英语语言包不能说汉语，同样汉语语言包不能说英语。
tts.setLanguage("English")
tts.say("Hello, world! I am Nao robot!")

# 切换语言包需要较长时间，故尽量不要在程序运行时切换；
#tts.setLanguage("Chinese")
#tts.say("你好，我是闹机器人。我可以说流利的绕口令：黑化肥挥发发灰会花飞")
