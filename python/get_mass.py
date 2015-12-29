#-*- coding: utf-8 -*-
from naoqi import ALProxy

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motionProxy = ALProxy("ALMotion", robot_ip, robot_port)

# ----------> get robot mass(质量) <----------
# Example showing how to get the mass of "HeadYaw".
pName = "HeadYaw"
mass = motionProxy.getMass(pName)
print pName + " mass: " + str(mass)

# Example showing how to get the mass "LLeg" chain.
pName = "LLeg"
print "LLeg mass: ", motionProxy.getMass(pName)

# It is equivalent to the following script
pNameList = motionProxy.getBodyNames("LLeg")
mass = 0.0
for pName in pNameList:
    jointMass = motionProxy.getMass(pName)
    print pName + " mass: " + str(jointMass)
    mass = mass + jointMass
print "LLeg mass:", mass
