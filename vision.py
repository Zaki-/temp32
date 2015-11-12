from pixy import *
from ctypes import *

import ctypes
import api
import os
import time
import sys
import struct


def Run(X,Y,Distance):
        global Walk, sit, HeadMoved,i,j
        #api.Walk(True)
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
		# call walk to the left till you reach pan = 512 (need while loop)
#		while (pan != 512):
			print "walk to the left"
	elif (pan<headLeftLim):
		# call walk to the right till you reach pan = 512 (need while loop)
#		while (pan != 512):
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
# Pixy Python SWIG get blocks example #

print ("Pixy Python SWIG Example -- Get Blocks")

# Initialize Pixy Interpreter thread #
pixy_init()

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

blocks = BlockArray(100)
frame  = 0

# Wait for blocks #
while 1:

  count = pixy_get_blocks(100, blocks)

  if count > 0:
    # Blocks found #
    print 'frame %3d:' % (frame)
    frame = frame + 1
    for index in range (0, count):
#      print '[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y, blocks[index].width, blocks[index].height)
    Type =  (blocks[index].type
    Sig =  blocks[index].signature
    X =  blocks[index].x
    Y =  blocks[index].y
    Width =  blocks[index].width
    Height =  blocks[index].height
    Run(X,Y,Width)


