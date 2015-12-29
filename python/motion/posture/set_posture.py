#-*- coding: utf-8 -*-
from naoqi import ALProxy

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

postureProxy = ALProxy("ALRobotPosture", robot_ip, robot_port)

# ----------> Set Posture <----------

postureProxy.goToPosture("StandInit", 1.0)
# std::string ALRobotPostureProxy::getPosture()
# Returns the name of the current predefined postures. 
# If the current posture is not in the predefined postures, it returns “Unknown”.
print "posture:", postureProxy.getPosture()

# Nao Robot H25, 支持的预设姿势
postureProxy.goToPosture("SitRelax", 1.0)
postureProxy.goToPosture("StandZero", 1.0)
postureProxy.goToPosture("LyingBelly", 1.0)
postureProxy.goToPosture("LyingBack", 1.0)
postureProxy.goToPosture("Stand", 1.0)
postureProxy.goToPosture("Crouch", 1.0)
postureProxy.goToPosture("Sit", 1.0)

print "posture list:", postureProxy.getPostureList()
print "robot posture family[now]:", postureProxy.getPostureFamily()
