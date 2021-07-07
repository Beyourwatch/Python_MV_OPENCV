from __future__ import print_function
import sys
from mvIMPACT import acquire
from mvIMPACT.Common import exampleHelper
import ctypes
import numpy
import cv2
import threading
import time

def opencamera(cameraindex, framecount):


    devMgr = acquire.DeviceManager()
    pDev = devMgr.getDevice(cameraindex)
    print(pDev.family.readS())
    pDev.interfaceLayout.writeS("GenICam")
    pDev.open()
    print("open camera" + str(cameraindex))
    framesToCapture = framecount

    fi = acquire.FunctionInterface(pDev)
    statistics = acquire.Statistics(pDev)
    imgformatControl = acquire.ImageFormatControl(pDev)
    imgdst = acquire.ImageDestination(pDev)
    acControl = acquire.AcquisitionControl(pDev)

    acControl.acquisitionFrameRate.writeS("10")
    imgdst.pixelFormat.writeS("RGB888Packed")

    while fi.imageRequestSingle() == acquire.DMR_NO_ERROR:
        print("Buffer queued")
    pPreviousRequest = None

    exampleHelper.manuallyStartAcquisitionIfNeeded(pDev, fi)

    cv2.namedWindow(str(cameraindex), cv2.WINDOW_NORMAL)
    cv2.resizeWindow(str(cameraindex), 500, 500)
    for i in range(framesToCapture):
        requestNr = fi.imageRequestWaitFor(10000)
        if fi.isRequestNrValid(requestNr):
            pRequest = fi.getRequest(requestNr)
            if pRequest.isOK:
                if i%100 == 0:
                    print("Info from " + pDev.serial.read() +
                         ": " + statistics.framesPerSecond.name() + ": " + statistics.framesPerSecond.readS() +
                         ", " + statistics.errorCount.name() + ": " + statistics.errorCount.readS() +
                         ", " + statistics.captureTime_s.name() + ": " + statistics.captureTime_s.readS())

            cbuf = (ctypes.c_char * pRequest.imageSize.read()).from_address(int(pRequest.imageData.read()))
            channelType = numpy.uint16 if pRequest.imageChannelBitDepth.read() > 8 else numpy.uint8
            arr = numpy.frombuffer(cbuf, dtype = channelType)

            arr.shape = (pRequest.imageHeight.read(), pRequest.imageWidth.read(), pRequest.imageChannelCount.read())
            cv2.imshow(str(cameraindex), arr)
            cv2.waitKey(10)


        if pPreviousRequest != None:
            pPreviousRequest.unlock()
        pPreviousRequest = pRequest
        fi.imageRequestSingle()
    else:
        print("imageRequestWaitFor failed (" + str(requestNr) + ", " + acquire.ImpactAcquireException.getErrorCodeAsString(requestNr) + ")")

    cv2.destroyWindow("Window")
    exampleHelper.manuallyStopAcquisitionIfNeeded(pDev, fi)





