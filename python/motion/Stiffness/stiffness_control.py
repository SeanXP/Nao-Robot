#-*- coding: utf-8 -*-
from naoqi import ALProxy
import time

# ----------> Connect to robot <----------
robot_ip = "192.168.1.100"
robot_port = 9559	# default port : 9559
motion = ALProxy("ALMotion", robot_ip, robot_port)

# ----------> Set stiffness <----------
# The robot will not move unless you set the stiffness of the joints to something that is not 0.

# void ALMotionProxy::setStiffnesses(const AL::ALValue& names, const AL::ALValue& stiffnesses)
# Parameters:
#	names - Names of joints, chains, “Body”, “JointActuators”, “Joints“Actuators”
#	stiffnesses - One or more stiffnesses between zero and one.

#motion.setStiffnesses("Body", 1.0) # 僵硬状态, 此时机器人的关节锁定，可以程序控制，不可人工移动。
#motion.setStiffnesses("Body", 0.0) # 非僵硬状态，此时可任意改变机器人的姿态，程序控制无效。

#motion.stiffnessInterpolation("Body", 0.0, 1.0) #阻塞一段时候(参数3)后调节某部位(参数1)的状态(参数2)
#与setStiffnesses()相比，先延迟一段时间，然后才设置状态;

#setStiffnesses()为非阻塞函数，立刻关闭/打开电机，这样可能有危险
#因此一般建议使用stiffnessInterpolation(), 并加上一段时间供机器人开关电机。

#stiffnesses = motion.getStiffnesses("Body") #获得关节的stiffness值

# ----------> Wake robot <----------

# Wake up robot
# sets Motor on and, if needed, goes to initial position. 唤醒电机，必要时进入初始姿态。
# 对于H25 NAO Robot, 将设置stiffness为开启状态，并恢复起始站立状态;
# 要执行wakeUp(), 则无需执行motion.setStiffnesses("Body", 1.0)
motion.wakeUp()
time.sleep(1)
print motion.getSummary() #打印机器人当前姿态
print "Robot is WakeUp? ", motion.robotIsWakeUp()

print motion.getStiffnesses("HeadYaw");
motion.setStiffnesses("HeadYaw", 0.0)
time.sleep(1)
print motion.getStiffnesses("HeadYaw");

# ----------> robot rest <----------
# 关闭电机，进入非僵硬模式，此后程序控制无效(因电机已关闭), 但可手工改变电机位置
# 进入复位状态(蹲伏动作)
motion.rest()
