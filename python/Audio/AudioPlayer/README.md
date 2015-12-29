[ALAudioPlayer](http://doc.aldebaran.com/2-1/naoqi/audio/alaudioplayer-api.html#alaudioplayer-api)
----

ALAudioPlayer provides playback services for multiple audio file format and the associated common functionalities (play, pause, stop, loop, etc...). The resulting audio stream is in all cases sent to the robot’s loudspeakers.


###Play

	aup = ALProxy("ALAudioPlayer", robot_IP, robot_PORT)

	fileId = aup.post.playFile("/home/nao/music/Maplestory.mp3")


`playFile(const std::string& fileName, const float& volume, const float& pan)`


	#音量volume, [0.0 - 1.0]
	#声道pan, (-1.0 : left / 1.0 : right / 0.0 : center)
	fileID = aup.playFile("/home/nao/music/Maplestory.mp3", 0.5, -1.0) # 重载函数
	
playFile()为阻塞调用，一般的用法是加post实现后台调用。    
记录好文件的FILEID，之后配置都会用到。

`playFileFromPosition(const std::string& fileName, const float& position)`,从特定位置开始播放音乐；

`playFileFromPosition(const std::string& fileName, const float& position, const float& volume, const float& pan)`

`playFileInLoop(const std::string& fileName)`，循环播放；   
`playFileInLoop(const std::string& fileName, const float& volume, const float& pan)`       


###Stop

`aup.stopAll()`
	
关闭所有的音乐。    
注意：Nao robot可以同时播放好几个音乐；

`pause(const int& taskId)`，暂停；

`play(const int& taskId)`，播放；    
`play(const int& taskId, const float& volume, const float& pan)`，播放；    


###Load
`loadFile(const std::string& fileName)`，返回fileID。    
预先装载文件，但不播放。    
预先装载可以有效减少播放音乐前所需的准备时间。    
装载好的文件可以直接play()播放。
	
	#Loads a file and launchs the playing 5 seconds later
	fileId = aup.loadFile("/usr/share/naoqi/wav/random.wav")
	time.sleep(5)
	aup.play(fileId)

`loadSoundSet(const std::string& setName)`，装载SoundSet。

`unloadAllFiles()`，unload所有文件；   
`unloadFile(const int& taskId)`；   
`unloadSoundSet(const std::string& setName)`；    

###Info

`getCurrentPosition(const int& taskId)`，返回现在文件播放的位置（秒数），非阻塞调用；

`getFileLength(const int& taskId)`，返回文件的长度（秒数）。

`getInstalledSoundSetsList()`，返回安装的soundset，一般返回['Aldebaran']。

**Soundset**   
A soundSet contains .ogg or .wav files.   
The Aldebaran soundSet is available trough the Basic Channel.

`getLoadedFilesIds()`，返回当前载入的文件列表taskID；   

`getLoadedFilesNames()`，返回当前载入文件的名称；   

playFile()的文件，不在LoadFile的统计之中；

`getLoadedSoundSetsList()`，返回当前载入的SoundSets。

`getMasterVolume()`，获得最大音量；  

`getVolume(const int& taskId)`，返回对应TASKID文件的音量；  

`goTo(const int& taskId, const float& position)`，跳到position秒位置；



###特殊

`playSine(const int& frequence, const int& gain, const int& pan, const float& duration)`，播放特定频率frequence，音量gain，声道pan，持续时间duration的正弦波。

可以通过该函数，实现一个测试人耳听力的小程序；

`playWebStream(const std::string& streamName, const float& volume, const float& pan)`，播放网络流音乐；

`setVolume(const int& taskId, const float& volume)`，设置音量；
`setMasterVolume(const float& volume)`，设置最大音量；


