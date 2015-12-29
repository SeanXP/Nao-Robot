ALAudioDevice
====

ALAudioDevice为其他NAOqi模块提供了访问NAO音频输入(麦克风)和音频输出(扬声器)的方法；   

如果有其他NAOqi模块想要处理麦克风信号或者给扬声器发信号，应该使用ALAudioDevice模块提供的API；    
（只有ALAudioPlayer具有自己的API控制扬声器，不需要调用ALAudioDevice模块的API）    

##How it works
ALAudioDevice基于Linux的ALSA库(Advanced Linux Sound Library)，来与Nao的声音驱动驱动通信，随后驱动麦克风与扬声器；

NAOqi模块通过调用相关API，可以发送数据给扬声器；

##Performances and Limitations
ALAudioDevice模块提供三个途径访问麦克风的数据：

* four channels interleaved, 48000Hz, 170ms buffer (this is the default setting)
* four channels deinterleaved, 48000Hz, 170ms buffer
* one channels (front, rear, left or right), 16000Hz, 170ms buffer

ALAudioDevice模块提供四个途径发送数据给扬声器：

* two channels interleaved, 16000Hz (default when an asian language is set)
* two channels interleaved, 22050Hz (default when a non asian language is set)
* two channels interleaved, 44100Hz
* two channels interleaved, 48000Hz

----

##API

`void ALAudioDeviceProxy::muteAudioOut(const bool& mute)`

静音；（静音后，tts.say函数无效，扬声器完全无声。）

`bool ALAudioDeviceProxy::isAudioOutMuted()`

----

`int ALAudioDeviceProxy::getOutputVolume()`     
获得音量；
（静音不会影响音量的改变）

