# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 06:59:34 2017

@author: Charles
"""
########### Python 3.2 #############

##take pic, send to server, return what it thinks it is
import picamera, time
camera = picamera.PiCamera()
camera.rotation = 180
   
 for i in range (0,20):
     
    camera.capture('/home/pi/image%s.jpg',i)
    print('captured picture %s',i)
    time.sleep(5)
   
    
