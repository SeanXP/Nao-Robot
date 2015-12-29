Stiffness control 
====

每个电机都有一个Stiffness值：

* Stiffness = 0, 电机控制关闭，此时电机不受程序控制，可以被任意转动。
* Stiffness = 1, 电机控制开启，此时电机受到程序控制，具有充足的扭矩力(full torque power)，不可被任意转动。    
* Stiffness在(0,1)区间内, 具有一定的扭矩力(扭矩力足够则电机达到目标位置, 扭矩力不够则电机无法达到目标位置)

控制Stiffness:

* 全局控制, 使用`ALMotionProxy::wakeUp()` 和 `ALMotionProxy::rest()`控制所有电机的开关状态。
* 局部控制, 使用`ALMotionProxy::stiffnessInterpolation()`, `ALMotionProxy::getStiffnesses()` 或 `ALMotionProxy::setStiffnesses()`.

wakeUp()将设置所有电机开启，rest()将设置所有电机关闭。(在机器人开发学习中，如果暂时不用机器人，可以使用rest()函数将机器人恢复到蹲伏姿态并关闭电机，节省电源及电机消耗。)

（Stiffness的控制是基于Naoqi的DCM(Device Communication Manager)模块。）


-----
###API

僵硬状态, 此时机器人的关节锁定，可以程序控制，不可人工移动。

	motion.setStiffnesses("Body", 1.0) 

非僵硬状态，此时可任意改变机器人的姿态，程序控制无效。
	
	motion.setStiffnesses("Body", 0.0) 

获得关节的stiffness值

	stiffnesses = motion.getStiffnesses("Body") 

阻塞一段时候(参数3, duration)    
与setStiffnesses()相比，先延迟一段时间，然后才设置状态;    
	
	motion.stiffnessInterpolation("Body", 0.0, 1.0)   


setStiffnesses()为非阻塞函数，立刻关闭/打开电机，这样可能有危险，因为当时机器人的状态不一定稳定，加上电机突然启动的剧烈振动可能导致机器人摔倒。    
因此一般建议使用stiffnessInterpolation(), 并加上一段时间供机器人开关电机。


获得所有关节状态
	
	print motion.getSummary()

`void ALMotionProxy::wakeUp()`   
`void ALMotionProxy::rest()`

----

###Events

* Event: "robotIsWakeUp"
* Event: "ALMotion/Stiffness/wakeUpStarted"
* Event: "ALMotion/Stiffness/wakeUpFinished"
* Event: "ALMotion/Stiffness/restStarted"
* Event: "ALMotion/Stiffness/restFinished"
* Event: "ALMotion/Protection/DisabledDevicesChanged"



