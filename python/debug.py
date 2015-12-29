#! /usr/bin/env python
#-*- coding: utf-8 -*-
from naoqi import ALProxy

robot_IP = "192.168.1.100"
robot_PORT = 9559	# default port : 9559

tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
motion = ALProxy("ALMotion", robot_IP, robot_PORT)
posture = ALProxy("ALRobotPosture", robot_IP, robot_PORT)
memory = ALProxy("ALMemory", robot_IP, robot_PORT)
leds = ALProxy("ALLeds", robot_IP, robot_PORT)
battery = ALProxy("ALBattery", robot_IP, robot_PORT)
autonomous = ALProxy("ALAutonomousLife", robot_IP, robot_PORT)
autonomous.setState("disabled") # turn ALAutonomousLife off

# 用于python交互命令行调试Naoqi API
# 使用方法，进入python交互命令行，执行: from debug import *
