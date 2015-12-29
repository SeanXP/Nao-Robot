ALPhotoCapture
===

ALPhotoCapture模块可以使得机器人拍摄图片并保存为文件存储在磁盘中；（只能保存在机器人内部）

----

## API
`AL::ALValue ALPhotoCaptureProxy::takePicture(const std::string& folderPath, const std::string& fileName)`     
拍摄照片    
参数：
 
* folderpath，图片保存路径；    
* fileName，图片文件名称；

如果文件已存在，则会被覆盖保存；    
不想覆盖文件，使用`ALPhotoCaptureProxy::takePicture(const std::string& folderPath, const std::string& fileName, const bool& overwrite)`，并设置overwrite=False；    


`AL::ALValue ALPhotoCaptureProxy::takePictures(const int& numberOfPictures, const std::string& folderPath, const std::string& fileName)`     
连续拍摄多张图片；     
同样有一个重载函数，最后多一个overwrite参数；    

多张图片名称将保存为: *xxx_0*, *xxx_1*, ...     

如果不设置图片参数，将使用默认参数：
	
* Camera ID: default (top camera)
* Color space: BGR
* Time between two pictures: 200 millisecond (i.e. 5 frames per second)
* Resolution: VGA (640 x 480)
* Picture format: jpg 

以上拍摄照片的API，都会花费一些时间（其函数内部要订阅ALVideoDevice模块，并等待一段时间等待摄像头图像稳定，最后还要取消订阅。）

为了加快速度，可以在调用拍摄API前自己订阅ALVideoDevice模块，这样将节省很多时间。
这种模式就是*halfpress*模式；    

* 设置*halfpress*模式为True，则会自动订阅模块；
* 设置*halfpress*模式为False，则会取消订阅模块；

*halfpress*模式下修改相关参数，如分辨率等是无效的，需要关闭*halfpress*模式再重新打开，才会生效；

**Warning:** 
小心使用*halfpress*模式模块，尤其是分辨率高的时候。因为*halfpress*模式可能会影响所有订阅ALVideoDevice的性能。
因此建议直到确定不再需要*halfpress*模式时，在关闭*halfpress*模式。


----
`void ALPhotoCaptureProxy::setPictureFormat(const std::string& pictureFormat)`     
设置图片的格式； 

pictureFormat – File format. Possible values are “bmp”, “dib”, “jpeg”, “jpg”, “jpe”, “png”, “pbm”, “pgm”, “ppm”, “sr”, “ras”, “tiff”, “tif”.

`std::string ALPhotoCaptureProxy::getPictureFormat()`

----
`void ALPhotoCaptureProxy::setResolution(const int& resolution)`     
resolution – New resolution { 0 = kQQVGA, 1 = kQVGA, 2 = kVGA }.    
设置图片分辨率:

* 0 = kQQVGA, Image of 160*120px
* 1 = kQVGA, Image of 320*240px
* 2 = kVGA , Image of 640*480px

`int ALPhotoCaptureProxy::getResolution()`

----
`void ALPhotoCaptureProxy::setCameraID(const int& cameraID)`     
设置要使用的摄像头；
Nao robot有两个摄像头可以使用:

* kTopCamera,  cameraID = 0
* kBottomCamera, cameraID = 1    

`int ALPhotoCaptureProxy::getCameraID()`

----

`void ALPhotoCaptureProxy::setCaptureInterval(const int& captureInterval)`    
设置拍摄的间隔时间，单位毫秒；    
默认为200ms, 即一秒拍摄5张图片；
 
 `int ALPhotoCaptureProxy::getCaptureInterval()`
 
 ----
 
`void ALPhotoCaptureProxy::setColorSpace(const int& colorSpace)`    
设置ColorSpace:    

* 0 = kYuvColorSpace, (for gray-scale images)
* 13 = kBGRColorSpace, (for color images)

`int ALPhotoCaptureProxy::getColorSpace()`

----

`bool ALPhotoCaptureProxy::setHalfPressEnabled(const bool& enable)`

配置*halfpress*模式

`bool ALPhotoCaptureProxy::isHalfPressEnabled()`



----

	photoCapture = ALProxy("ALPhotoCapture", robot_IP, robot_PORT)
	
	# Take 3 pictures in VGA and store them in ./
	# 设置分辨率，{ 0 = kQQVGA, 1 = kQVGA, 2 = kVGA }
	photoCapture.setResolution(2)
	
	# 设置图片格式，“bmp”, “dib”, “jpeg”, “jpg”, “jp, 等等
	photoCapture.setPictureFormat("jpg")
	
	photoCapture.takePictures(3, "/home/nao/recordings/cameras/", "image")


	