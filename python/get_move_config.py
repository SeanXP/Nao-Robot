#-*- coding: utf-8 -*-
from naoqi import ALProxy
import time

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motionProxy = ALProxy("ALMotion", robot_ip, robot_port)
# ----------> <----------

# get move config
# AL::ALValue ALMotionProxy::getMoveConfig(const std::string& config)
#
# 参数: config - a string should be "Max", "Min", "Default" 
# 返回格式
#[ ["MaxStepX", value],
#  ["MaxStepY", value],
#  ["MaxStepTheta", value],
#  ["MaxStepFrequency", value],
#  ["StepHeight", value],
#  ["TorsoWx", value],
#  ["TorsoWy", value]
#]  
#
print motionProxy.getMoveConfig("Default")
# Nao Robot Default Move Config
# [
# 	['MaxStepX', 0.03999999910593033], 
#	['MaxStepY', 0.14000000059604645], 
#	['MaxStepTheta', 0.3490658402442932], 
# 	['MaxStepFrequency', 1.0], 
#	['StepHeight', 0.019999999552965164], 
#	['TorsoWx', 0.0], 
#	['TorsoWy', 0.0]
# ]

#####################

# 另一种用法
# a getFootConfig could be directly use in a walk method
#motionProxy.moveInit() # 初始化移动进程，检查机器人的姿势并切换为正确的姿势。
# 配置为Min, 最小的走路速率, 相当于原地踏步
#motionProxy.moveToward(1.0, 0.0, 0.0, motionProxy.getMoveConfig("Min")) 
#time.sleep(3.0)
#motionProxy.stopMove()
