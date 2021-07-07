from __future__ import print_function
import sys
from mvIMPACT import acquire
from mvIMPACT.Common import exampleHelper
import ctypes
import numpy
import cv2
import threading
import ContinuousCapture as camera


exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, Cameraindex, framecount):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.cameraindex = Cameraindex
        self.framecount = framecount
    def run(self):
        print ("开始线程：" + self.name)
        camera.opencamera(self.cameraindex, self.framecount)
        print ("退出线程：" + self.name)



# 创建新线程

thread1 = myThread(1, 0, 100)
thread2 = myThread(2, 1, 100)

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("退出主线程")


cv2.waitKey()
