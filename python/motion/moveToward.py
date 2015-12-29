#-*- coding: utf-8 -*-
from naoqi import ALProxy
import time
import argparse # 命令行参数解析

""" moveToward()函数用法示例
	void ALMotionProxy::moveToward(const float& x, const float& y, const float& theta)
	控制机器人以给定的速率移动（归一化的单位，并非m/s，与moveToward()的区别），参考系w为FRAME_ROBOT；非阻塞函数。
	参数x, X轴的速率(+1表示正方向的最大速率, -1为反方向)。向X轴负方向则使用负速率。
	参数y, Y轴的速率。
	参数theta, 绕Z轴旋转的速率。（单位：弧度radians/s）逆时针为正，顺时针为负。

	重载函数:
	void ALMotionProxy::moveToward(const float& x, const float& y, const float& theta, const AL::ALValue moveConfig)


	本程序中，先以正常频率(frequency = 1.0)行走，然后切换为慢频率(frequency = 0.5)行走;

"""

def main(robotIP, PORT=9559):
    motionProxy  = ALProxy("ALMotion", robotIP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

# 	motionProxy.moveInit()

    # Example showing the use of moveToward
    # The parameters are fractions of the maximums
    # Here we are asking for full speed forwards, 即x = 1.0
    x     = 1.0
    y     = 0.0
    theta = 0.0
    frequency = 1.0
    motionProxy.moveToward(x, y, theta, [["Frequency", frequency]])

    # If we don't send another command, he will move forever
    # Lets make him slow down(step length) and turn after 3 seconds
    time.sleep(3) # 延时3秒运动

    x     = 0.5
    theta = 0.6
    motionProxy.moveToward(x, y, theta, [["Frequency", frequency]])

    # Lets make him slow down(frequency) after 3 seconds
    time.sleep(3)
    frequency = 0.5 # 频率1为最快, 0.5表示50%的频率运动
    motionProxy.moveToward(x, y, theta, [["Frequency", frequency]])

    # Lets make him stop after 3 seconds
    time.sleep(3)
    motionProxy.stopMove()

	# 详细的Move Config配置
	##################################
	#
    # TARGET VELOCITY
    X         = 1.0
    Y         = 0.0
    Theta     = 0.0
    Frequency = 1.0

    # Defined a limp walk
    try:
        motionProxy.moveToward(X, Y, Theta,[["Frequency", Frequency],
                                            # LEFT FOOT
                                            ["LeftStepHeight", 0.02],
                                            ["LeftTorsoWy", 5.0*almath.TO_RAD],
                                            # RIGHT FOOT
                                            ["RightStepHeight", 0.005],
                                            ["RightMaxStepX", 0.001],
                                            ["RightMaxStepFrequency", 0.0],
                                            ["RightTorsoWx", -7.0*almath.TO_RAD],
                                            ["RightTorsoWy", 5.0*almath.TO_RAD]] )
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()



    motionProxy.stopMove()
    # Note that at any time, you can use a moveTo command
    # to run a precise distance. The last command received,
    # of velocity or position always wins

    # Go to rest position
    motionProxy.rest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.100",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
