Nao Robot - xpServer
====
移动应用控制Nao机器人

* ChatRobot.py， 聊天机器人模块，提供SimSimi与图灵机器人两个聊天机器人引擎。需要在对应官方主页申请API KEY。这里没有提供settings.py文件；
* MP3_Player.py，音乐播放模块；
* avoidance_module.py， 超声波简单避障模块；
* leds.py， LED灯模块；
* touch_password.py，触摸登录模块；
* video_module.py，视频发送模块；
* xpserver.py，服务器模块；

服务器端主程序为xpserver.py，其中调用了其他模块的相应函数；

----
socket TCP port: 8001，发送命令端口;
socket UDP port: 8003,  视频传输端口;

手机端连接TCP port: 8001，向机器人发送相应指令以控制机器人；
