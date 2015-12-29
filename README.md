Nao Robot H25 V5
====

参考网站：  
[aldebaran](http://www.aldebaran.com/)  
	要访问官网的讨论区以及资源，都需要登录。
	
[Ros-nao](http://wiki.ros.org/nao) 

----


# [Upgrading my NAO](http://doc.aldebaran.com/2-1/embedded/upgrade.html)

Once your NAO has been updated with a 2.x release, you can use the new Aldebaran Cloud to set an automatic system update.

For further details, see: [Setting automatic system update](http://doc.aldebaran.com/2-1/nao/nao_store_sysupdate.html#nao-store-sysupdate).   

设置自动更新后，如果有可以更新的版本，机器人会自动下载相应的更新镜像，可以通过查看机器人的网速看其是否在自动下载。   
下载的镜像存放在机器人系统目录`/var/persistent/.image`路径下。同时在该目录查看系统升级日志upgrade.log。下载完成以后，需要重启机器人，重启过程中机器人会检测镜像并升级；

Nao 2.x以后的版本，都是在机器人web管理页面下载更新包进行更新。

----
