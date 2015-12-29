#-*- coding: utf-8 -*-
from naoqi import ALProxy

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559			# default port : 9559

motion = ALProxy("ALMotion", robot_ip, robot_port)
posture = ALProxy("ALRobotPosture", robot_ip, robot_port)
navigation = ALProxy("ALNavigation", robot_ip, robot_port)

# ----------> stand init <----------

# Wake up robot
motion.wakeUp()

# Send robot to Stand Init
posture.goToPosture("StandInit", 0.5)

# Move-1: No specific move config, just move 1 meter in x-axis.
motion.moveTo(1.0, 0.0, 0.0)
motion.moveTo(1.0, 0.0, 0.0, [])

# Move-2: To do 6 cm steps instead of 4 cm. 步子迈大咯
motion.moveTo(1.0, 0.0, 0.0, [["MaxStepX", "0.06"]])

# Will stop at 0.5m (FRAME_ROBOT) instead of 0.4m away from the obstacle.
# 设置安全距离为0.5m, 遇到障碍物在0.5m内则停止.
navigation.setSecurityDistance(0.5)
# ALNavigation模块基本都是用于Pepper机器人，Nao机器人基本不用。
# ALNavigationProxy::setSecurityDistance()函数，也从Naoqi version 1.22版本后被废弃
# 替代的API为： ALMotionProxy::setOrthogonalSecurityDistance
