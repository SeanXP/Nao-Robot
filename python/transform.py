#-*- coding: utf-8 -*-
from naoqi import ALProxy
import argparse
import time
import almath

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
motion = ALProxy("ALMotion", robot_ip, robot_port)
posture = ALProxy("ALRobotPosture", robot_ip, robot_port)

# ----------> set a posture <----------
motion.wakeUp()
posture.goToPosture("StandInit", 0.5)

# ----------> Retrieve a transform matrix using ALMotion <----------
chainName = "RArm"
frame = 1 # FRAME_WORLD
useSensors = True

# Retrieve current transform from ALMotion.
# Convert it to a transform matrix for ALMath.
origTransform = almath.Transform(motion.getTransform(chainName, frame, useSensors))
# std::vector<float> ALMotionProxy::getTransform(
# 			const std::string& name, const int& frame, const bool& useSensorValues);
# Gets an Homogeneous Transform relative to the FRAME. 
# Axis definition: the x axis is positive toward the robot’s front, the y from right to left and the z is vertical.
# 	
#	name - Name of the item. Could be: any joint or chain or sensor
# 	frame -  Task frame {FRAME_TORSO = 0, FRAME_WORLD = 1, FRAME_ROBOT = 2}.
# 	useSensorValues - If true, the sensor values will be used to determine the position.
#
# Returns:	
#	Vector of 16 floats corresponding to the values of the matrix, line by line.

print "Original transform"
print origTransform

# ----------> use almath to do some computations on transform matrix <----------
# Compute a transform corresponding to the desired move
# (here, move the chain for 5cm along the Z axis and the X axis).
# 计算从当前位置到目标位置(X移动0.05m, Z移动0.05m)所需要的转换;
moveTransform = almath.Transform.fromPosition(0.05, 0.0, 0.05)
targetTransform = moveTransform * origTransform

print "Target transform"
print targetTransform

# ----------> Send a transform to the robot via ALMotion <----------
# Convert it to a tuple.
targetTransformList = list(targetTransform.toVector())

# Convert it to a tuple.
fractionOfMaxSpeed = 0.5
axisMask = almath.AXIS_MASK_VEL # Translation X, Y, Z
motion.setTransforms(
	chainName,
    frame,
    targetTransformList,
    fractionOfMaxSpeed,
    axisMask)

time.sleep(2.0)
motion.rest()
