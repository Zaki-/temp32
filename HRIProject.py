#  HRI Project 
#  By Anmar AlZubaidi - Hussain Zaki - Fangyu

import numpy as np
import cv2
import ctypes
import api
import os
import time
import sys
import struct


# local modules
from video import create_capture
from common import clock, draw_str

help_message = '''
USAGE: facedetect_edit.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
''' 
global Walk, sit, HeadMoved,p,j
def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
def Run(X,Y,Distance):
        global Walk, sit, HeadMoved,i,j
        print("Running...")
        command = 0
	z=5
	# declaring servos limmits
	#headRightLim=667
	#headLeftLim=364
	#headUpLim=612
	#headDownLim=433
	
	headRightLim=600
        headLeftLim=420
        headUpLim=612
        headDownLim=433
        
        
	pan = api.GetMotorValue(19)
	tilt= api.GetMotorValue(20)
	
	# check when to call the walk functions
        if ((pan<headRightLim) and (pan>headLeftLim)):
		print "head move"
	elif (pan>headRightLim):
			print "walk to the left"
	elif (pan<headLeftLim):
                        print "walk to the left"
	if (abs(X)>=100): p=9
	elif (abs(X)<100 and abs(X) >70): p = 7
	elif (abs(X)<= 70 and abs(X)> 50): p= 5
	else: p=2
	if (abs(Y)>=100): j=5
        elif (abs(Y)<100 and abs(Y) >70): j = 4
        elif (abs(Y)<= 70 and abs(Y)> 50): j= 3
        else: j=2
	print ('p = ',p, 'j= ',j)
	if HeadMoved == 0:
	   i= int(round(X/10))
	   if (X>50) and (667 > pan):
		for I in range(1,z):
			api.SetMotorValue(19,pan+p)
	   elif (X<-50) and (364 < pan):
		for I in range(1,abs(z)):
			api.SetMotorValue(19,pan-p)
	   if (Y>50) and ( 612 > tilt):
                for I in range(1,z):
                        api.SetMotorValue(20,tilt+j)
           elif (Y<-50) and (433 < tilt):
                for I in range(1,abs(z)):
                        api.SetMotorValue(20,tilt-j)
	print Distance
	if (Distance < 150) and (Walk == False):
		api.Walk(True)
		speed = int((150-Distance)/2)
		if speed > 10: speed = 10
		print ('Speed = ',speed)
		api.WalkMove(speed)
		Walk = True
		sit = 0
		HeadMoved = 1
		print('Walk=======>')
	elif(Distance > 150) and (Walk == True)  :
		#api.WalkMove(2)
		#api.Walk(False)
		Walk=False	
		if (sit == 0):
			api.Walk(False)
			api.PlayAction(15)
			sit = 1
			print ( 'Sitting+++++++++')
	if (Walk == True):
		if (X>50):
                         api.WalkTurn(p)
                         #api.WalkMove(Distance)
			 print('Trun Right')
                elif (X<-50):
                         api.WalkTurn(-p)
                         print('Trun Left')
                else :
                        api.WalkTurn(0)
                        print ('No Trun')

        print("pan",pan)

        print("tilt",tilt)
        #api.ServoShutdown()

	
	#Run()
if __name__ == '__main__':
    import sys, getopt
    Walk = False
    sit = 0
    HeadMoved = 0
    i=1
    j=1
    print help_message
    try:
                if api.Initialize():
                        print("Initalized")
                else:
                        print("Intialization failed")

    except (KeyboardInterrupt):
                api.ServoShutdown()
                sys.exit()
    except():
        api.ServoShutdown()
        sys.exit()
    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try:
        video_src = video_src[0]
    except:
        video_src = 0
    args = dict(args)
    cascade_fn = args.get('--cascade', "../../../../../opencv/data/haarcascades/haarcascade_frontalface_alt.xml")
    nested_fn  = args.get('--nested-cascade', "../../../../../opencv/data/haarcascades/haarcascade_eye.xml")

    cascade = cv2.CascadeClassifier(cascade_fn)
    nested = cv2.CascadeClassifier(nested_fn)

    cam = create_capture(video_src, fallback='synth:bg=../../../../../opencv/data/lena.jpg:noise=0.05')
    try:
    	while True:
		#break
	
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            t = clock()
            dt = clock() - t
 
            rects = detect(gray, cascade)
            vis = img.copy()
            draw_rects(vis, rects, (0, 255, 0))
            if not nested.empty():
                for x1, y1, x2, y2 in rects:
                    roi = gray[y1:y2, x1:x2]
                    vis_roi = vis[y1:y2, x1:x2]
                    subrects = detect(roi.copy(), nested)
                    #draw_rects(vis_roi, subrects, (255, 0, 0))
                    # print ('time: %.1f ms' % (dt*1000))
                    # print ('Length: %.1f cm' % (y2-y1))
                
		    x_center=(320-(x2+x1)/2)
		    y_center=(240-(y2+y1)/2)
		    Run(x_center,y_center,y2-y1)
		    #print (x_center,y_center)
            if 0xFF & cv2.waitKey(5) == 27:
                break
        cv2.destroyAllWindows()
    except (KeyboardInterrupt):
		print
		print ("ID 20 :", api.GetMotorValue(20))

                api.ServoShutdown()
                sys.exit()
# this steps to read servo's value-- add break to the maim while then uncomment the next two lines
#print (api.GetMotorValue(20))
#api.ServoShutdown()
