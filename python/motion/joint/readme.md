Nao Robot Joint Control
----

可以单独的控制一个关节的位置(指定关节的名称)，也可以并行控制(指定一组关节的组名称, 例如"Body")。

##两种控制方法

1. animation methods (time fixed, blocking function)
	* `ALMotionProxy::angleInterpolation()`
	* `ALMotionProxy::angleInterpolationWithSpeed()`
2. reactive methods (could be changed every ALMotion cycle, non blocking function)
	* `ALMotionProxy::setAngles()`
	* `ALMotionProxy::changeAngles()`

关节控制的工作原理是基于Naoqi的DCM模块.

----

##Naoqi API
####获得Body的所有关节名称
	motion.getBodyNames(“Body”)

	
['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']

	# 示例程序
	motionProxy.setStiffnesses("Head", 1.0)
	# Simple command for the HeadYaw joint at 10% max speed
	names = "HeadYaw"
	angles = 90.0 * almath.TO_RAD # 角度转弧度
	fractionMaxSpeed = 0.1	
	motionProxy.setAngles(names,angles,fractionMaxSpeed) # 以10%的速度转换30角度
	# setAngles()为非阻塞函数, 故需延时等待.
	time.sleep(3.0)
	motionProxy.setStiffnesses("Head", 0.0)
	motionProxy.rest() # 恢复为初始蹲伏状态


设置names关节转动到指定弧度angles, 限制最大速度为fractionMaxSpeed;    
`void ALMotionProxy::setAngles(const AL::ALValue& names, const AL::ALValue& angles, const float& fractionMaxSpeed)`    
Sets angles. This is a non-blocking call. 非阻塞函数;    
其中设置的角度是相对初始状态而言的，因此如果上一次执行成功，下次再执行就没有效果了。

changeAngles()的用法与setAngles()用法相同，唯一不同点在于：    

* setAngles()的参数是绝对弧度，多次调用不影响结果；    
* changeAngles()的参数是相对弧度，多次调用影响结果，每次调用都会移动。    
由于changeAngles()与setAngles()均为**非阻塞函数**，多次调用不会影响线程调度（函数执行期间再次调用相同参数的函数不影响结果，调用方向相反的函数则中止上次调用，即机器人总是确保轨迹平滑并符合要求）

.

	names = "HeadYaw"
	angleLists = [1.0, -1.0, 1.0, -1.0, 0.0]
	times      = [1.0,  2.0, 3.0,  4.0, 5.0]
	isAbsolute = True
	motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)



	# Head Start to zeros
	names             = "Head"
	targetAngles      = [0.0, 0.0]
	maxSpeedFraction  = 0.2 # Using 20% of maximum joint speed
	motionProxy.angleInterpolationWithSpeed(names, targetAngles, maxSpeedFraction)

获得关节角度值    
`std::vector<float> ALMotionProxy::getAngles(const AL::ALValue& names, const bool& useSensors)`
Gets the angles of the joints    
Parameters:       
names – Names the joints, chains, “Body”, “JointActuators”, “Joints” or “Actuators”.    
useSensors – If true, sensor angles will be returned    
Returns:        
Joint angles in radians.    
第二个参数useSensors=True, 则返回传感器检测的角度值；   useSensors=False, 则返回该关节的理论角度值(理论与实际的角度值会有一些误差出入)。   


	# 张开手指, 同时关闭电机电流以节省能量；阻塞调用函数；
	motionProxy.openHand("LHand")
	motionProxy.openHand("RHand")
	motionProxy.closeHand("LHand")
	motionProxy.closeHand("RHand")

	