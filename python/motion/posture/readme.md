ALRobotPosture
====

ALRobotPosture, 在姿势层次控制机器人。主要API为控制机器人实现预设姿势。    

ALRobotPosture可以设置机器人的姿态；

* `ALRobotPostureProxy::goToPosture()` 使得机器人自主的达到一个姿态(机器人检测当前姿态，然后计算一条到达目的姿态的路径，然后不断调节姿态，最终到达指定姿态)
* `ALRobotPostureProxy::applyPosture()` ，快速改变机器人姿态。没有过渡状态，因此机器人很容易跌倒。（建议手扶着）

###Predefined postures 预设姿势
Here is the list of the Predefined Postures names:

* Crouch, 蹲伏
* LyingBack,
* LyingBelly,
* Sit,
* SitRelax,
* Stand,
* StandInit,
* StandZero.

（官方网站上可以查看预设姿势, Nao H25 Robot全部支持）

由于某种机器人不支持一些预设姿态，因此建议使用`ALRobotPostureProxy::getPostureList()`确认机器人所支持的预设姿势。

Nao H25 Robot    
['Crouch', 'LyingBack', 'LyingBelly', 'Sit', 'SitOnChair', 'SitRelax', 'Stand', 'StandInit', 'StandZero']

由于理论上的姿势具有无限多种可能，因此为了便于区分当前的姿势，使用**姿势族(Posture family)**这一概念。
使用`ALRobotPostureProxy::getPostureFamilyList()`查看当前机器人可用的Posture family.

###API
获得机器人预设姿势列表     
`std::vector<std::string> ALRobotPostureProxy::getPostureList()`

获得机器人的当前姿态。如果是预设姿态，则返回特定姿势名称，若非预设姿势，则返回'Unknown'      
`std::string ALRobotPostureProxy::getPosture()`     

控制机器人到达指定姿态；     
参数1为姿态名称，参数2为切换姿态的速度(0 ~ 1.0)；    
goToPosture()切换姿态是智能的，计算出到达目的姿势所需要的移动路径，进行改变。    
阻塞调用，返回是否成功，成功返回True, 失败返回False.    
`bool ALRobotPostureProxy::goToPosture(const std::string postureName, const float speed)`


切换姿势。此操作立刻切换（即立刻更改各个关节值），可能会使机器人跌倒。     
`bool ALRobotPostureProxy::applyPosture(const std::string& postureName, const float& speed)`     

立刻停止当前的姿势更改。    
`void ALRobotPostureProxy::stopMove()`

Posture Family相关：    
`ALRobotPostureProxy::getPostureFamily()`，    `ALRobotPostureProxy::getPostureFamilyList()`

###Event

Event: "**PostureFamilyChanged**"    
Raises the name of the Posture family when it changes.    
当机器人的Posture Family更改时会触发该事件，事件触发频率1HZ;    

Event: "**PostureChanged**"    
姿势更改触发时间，触发频率1HZ，即1s更新一次；

