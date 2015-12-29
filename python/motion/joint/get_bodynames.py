#-*- coding: utf-8 -*-
from naoqi import ALProxy

# ----------> Connect to robot <----------
robot_ip = "192.168.2.100"
robot_port = 9559			# default port : 9559

motion = ALProxy("ALMotion", robot_ip, robot_port)

# Example showing how to get the names of all the joints in the body.
bodyNames = motion.getBodyNames("Body")
print "Body:"
print str(bodyNames)
print ""

# Example showing how to get the names of all the joints in the left leg.
leftLegJointNames = motion.getBodyNames("LLeg")
print "LLeg:"
print str(leftLegJointNames)
print ""

####### Joints
# Head
# LArm
# RArm
# LLeg
# RLeg
