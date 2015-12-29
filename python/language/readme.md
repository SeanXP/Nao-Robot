language
===

	tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
	tts.setLanguage("Chinese")
	tts.setLanguage("English")

切换语言包需要较长时间，故尽量不要在程序运行时切换；    
经过测试，切换汉语包需要2秒，切换英语包需要0.8秒；   
另外，下载的英语包为一百多兆，而汉语包只有十兆；     
尽量使用英语包；       
English->Chinese: 2.00102996826   
Chinese->English: 0.818722009659   