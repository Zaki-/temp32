import sys

#appends api directory path to sys path
#sys.path.append("/home/pi/Human_Robots_Interaction_Fall15")
sys.path.append("/home/pi/HROS1-Framework/Linux/project/Human_Robots_Interaction_Fall15")


import api 

from collections import deque

from pixy import *
from ctypes import *

tempY=0
speedInc=0
timer = 0
chestX = 0
chestY=0
HeadY=0
LHX=0
RHX=0
LHY=0
RHY=0


def RoboWalk(color, trackX):   # X,Y are the center of the object that is deteced by pixy, color green move, color red stop
    global sit, walk, speedInc, timer
 #   timer = timer +1
  #  print  timer
    if (color == 'green') and (walk == False): #if the color is green and the robot is not walking let it walk

        api.Walk(True)       # set the robot in walk ready mode
	speed =10
        api.WalkMove(speed)  #the robot start to move for the given speed
        walk = True          #indicate that the robot is walikg
        sit=0                #flag that the robot is not in sit position
        #HeadMove = False     
    elif (color == 'red') and (walk == True):  #
       walk = False         #indicate that the robot not walking
       if (sit == 0):       #if the robot is not in sit position make it sit
        api.Walk(False)    #stop the walk ready mode
        api.PlayAction(15) #call the sit position - page 15
        sit=1              # flag that the robot is in sit position

#def RoboTurn(trackX):
    # Turn while walking
    if (walk == True): #if the robot is walking check the direction 
        if (trackX>10):
    	    api.WalkTurn(-5)
	    
	    print 'left'
        elif(trackX<-10):
            api.WalkTurn(5)
	    print 'right'
        else :
            api.WalkTurn(0)
#	End of RoboWalk()

def RoboInit():
    try:
                if api.Initialize():
                        print("Initalized")
			api.PlayAction(50)
                else:
                        print("Intialization failed")

    except (KeyboardInterrupt):
                api.ServoShutdown()
                sys.exit()
    except():
        api.ServoShutdown()
        sys.exit()

# End of RoboInit()
# set the Global variables
def centerX(x):
	return x-160
def centerY(y):
	return 100-y
sitFlag =True #start with the sitting position
walkFlag =False

def SetHead(x,y):
	pan=api.GetMotorValue(19)
	tilt= api.GetMotorValue(20)
	if (x>20) and (pan <600) and (pan>390):
		for i in range(1, 5):
 			api.SetMotorValue(19,pan-1)
	elif (x<-20) and (pan >380) and (pan <600):
		for i in range(1, 5):
			api.SetMotorValue(19,pan+1)
	if (y>20) and (tilt < 612) and (tilt >420):
		for i in range(1, 5):
			api.SetMotorValue(20,tilt-1)
	elif (y<-20) and (tilt > 420) and (tilt < 612):
		for i in range(1, 5):
			api.SetMotorValue(20,tilt+1)
	print 'tilt=',tilt

def WalkReady(b):
	global walkFalg,startCounter
	# counter to stop walking by itself after it counts 3000 frames
	startCounter=frame
	if (frame-startCounter) == 3000 :
		b=False
	# end of the counter
	if (b == True) and (walkFlag == False) and (sitFlag == False) :
		api.Walk(True)
		api.WalkMove(3)
		walkFlag = True
	elif (b == False) and (walkFlag == True) and (sitFlag == False):
		api.Walk(False)
		api.PlayAction(2)
		walkFlag = False



def Sit(b):#pass true to make the robot sit and False to make it stand
	global sitFlag
	if (b == True) and (sitFlag == False):
		api.PlayAction(16)
		sitFlag = True
	elif (b == False) and (sitFlag ==True):
		api.PlayAction(2)
		sitFlag = False
		

def SoS():
	if (sitFlag == False) and (walkFlag == False):
		print 'api.PlayAction(sos)'

def UVA():
	if (sitFlag == False) and(walkFlag == False):
		api.PlayAction(80)


sitFLAG=True
standFLAG=False
introFLAG=False
walkFLAG=False
frame = 0
def checkSign2(LHY, LHarea,RHY, RHarea,HeadY, Headarea,chestY, chestarea, frame):
	#one of the chalenges is the rate of the edges must change with the distance
	global sitFLAG, standFLAG, introFLAG
	HY=abs(LHY-RHY)
	avg=abs(int((LHY+RHY)/2))
	rateY=abs(HeadY-chestY)
	# stand up
	if (abs(LHY-chestY)<8)and (standFLAG==False) :
		print 'stand'
		print 'frame=%d' %(frame)
		standFLAG=True
#		WalkReady(False)
#		sit(False) #stand
	# sit down
	if (LHY > (chestY+20)) and (standFLAG == True):
	#if (abs(chestY-LHY)-abs(int(0.3*rateY))<5):
	#if (HY > 10) and (LHY>chestarea):
	#if (HY<10) and (abs(chestY-HY)-abs(int(0.3*rateY))<10) and (avg > chestY) and (avg > HeadY):
	#the distance between chestY and both hands Y(HY) almost equels half of distance between head and chest
		print 'sit'
		print 'frame=%d' %(frame)
		standFLAG = False
#		WalkReady(False)
#		sit(True)
	# start walking
	if (LHY > HeadY+15 ) and (LHY < chestY-15) and (standFLAG == True) :
	#if (HY<10) and (abs(HeadY-HY)-abs(int(0.3*rateY))<10) and (avg>HeadY) and (avg < chestY):
	# the distance between head and both hands Y almost equels half of  the distance between the head and chest 
		print 'walking'
		print 'frame=%d' %(frame)
		standFLAG=False
#		WalkReady(True)


	# UVA
#	if (HY<10) and (RHX == LHX) and (HY > chestY):
#		UVA()
	# SoS
	if (LHY < HeadY-10) and (standFLAG == True):
#	if (HY<10) and (abs(HeadY-HY)-abs(int(0.3*rateY))<10) and (avg<HeadY) and (avg < chestY):
		print 'sos'
		print 'frame=%d' %(frame)
		standFLAG=False
#		SoS()

	# Introduction
	if (RHY >HeadY+15 ) and (RHY <chestY-15) and (standFLAG == False) and (introFLAG == False):
		introFLAG = True
		print 'stand'
#		api.PlayAction(2)
		print 'wave'
#		api.PlayAction('wave')
		print 'sit'
#		api.PlayAction(16)

command=['1','1','1','1','1']
def checkSign(LHY,RHY, HeadY, chestY):
	global introFLAG, command, walkFLAG, standFLAG
	#intro
	if (abs(RHY-chestY)<8 ) and (introFLAG==False):
		introFLAG=True
		print 'stand'
		api.PlayAction(44)
		print 'wave'
		api.PlayAction(25)
		print 'sit'
		api.PlayAction(50)
	#sit -1-
	if (LHY > (chestY+20)):
		command.append('1')
#		command.popleft()
		command=command[1:]
	#stand -2-
	if (abs(LHY-chestY)<8):
		command.append('2')
#		command.popleft()
		command=command[1:]
	#walk -3-
	if (LHY > HeadY+15 ) and (LHY < chestY-15) :
		command.append('3')
#		command.popleft()
		command=command[1:]
	#UVA -4-
	if (LHY > (HeadY-10)) and (LHY < (HeadY+10)):
		command.append('4')
#		command.popleft()
		command=command[1:]
	#SoS -5-
	if (LHY < HeadY-10):
		command.append('5')
#		command.popleft()
		command=command[1:]
		
	#check the command
	
	if (command == ['1','1','1','1','1']) and (standFLAG == True):#sit -1-
		print 'sit'
		api.PlayAction(50)
		standFLAG=False
	elif (command == ['2','2','2','2','2']) and (standFLAG == False) and (walkFLAG==False):#stand -2-
		print 'stand'
		api.PlayAction(44)
		standFLAG=True
	elif (command == ['2','2','2','2','2']) and (walkFLAG== True) and (standFLAG == False):#stop walking
		print 'stop and stand'
		api.Walk(False)
		api.PlayAction(44)
		walkFLAG = False
		standFLAG=True
	elif (command == ['3','3','3','3','3']) and (standFLAG == True) and (standFLAG==True):#walk -3-
		print 'walk'
		api.Walk(True)
		api.WalkMove(0)
		walkFLAG = True
		standFLAG=False
	elif (command == ['4','4','4','4','4']) and (standFLAG==True):#UVA -4-
		print 'UVA'
		UVA()
		standFLAG=False
	elif (command == ['5','5','5','5','5']) and (standFLAG==True):#SoS -5-
		print 'SOS'
		UVA()
		standFLAG=False
	

sit = 0
walk = False
X=0  # 0 - 320
color = 'red'
LHarea=0
RHarea=0
Headarea=0
chestarea=0
temparea=0

#initialize Pixy interpreter thread
pixy_init()

#initialize the Robot movements
RoboInit()

#Blocks
class Blocks (Structure):
      _fields_ = [ ("type", c_uint),
                   ("signature", c_uint),
                   ("x", c_uint),
                   ("y", c_uint),
                   ("width", c_uint),
                   ("height", c_uint),
                   ("angle", c_uint) ]

blocks = BlockArray(100)
frame = 0
battryLim = 107
#wait for blocks
#api.SetMotorValue(20,433)
try:
  while 1:
     count = pixy_get_blocks(100, blocks)
#     if (int(api.BatteryVoltLevel()) <= battryLim):
#      if (int(api.BatteryVoltLevel()) <= battryLim):
#       if (int(api.BatteryVoltLevel()) <= battryLim):

#	print 'Low Battery'
#	api.Walk(False)
#	api.PlayAction(15)
#	api.ServoShutdown()
#	sys.exit()
#     else:
#       print 'Battery power', int(api.BatteryVoltLevel())
     if count > 0:
#	 
         #blocks found
	 Uframe=frame/500
         #print 'frame %3d:' % (frame)
         frame = frame +1
	 				
	 if (frame % 500) == 0:
		 print '====================================='
		 checkSign(LHY,RHY, HeadY, chestY)
		 print 'RHY=%d LHY=%d chestY=%d HeadY=%d' %(RHY, LHY, chestY, HeadY)
		 print command

         for index in range(0, count):
		# pixy reselution 320X200	     

             	if (index == 0) and (blocks[index].signature == 1) and (blocks[index].x < chestX):
			RHX=blocks[index].x
			RHY=blocks[index].y
			RHarea=blocks[index].height*blocks[index].width
		if (index == 1) and (blocks[index].signature == 1) and (blocks[index].x >= chestX):
			LHX=blocks[index].x
			LHY=blocks[index].y
			LHarea=blocks[index].height*blocks[index].width

		if (index == 2) and (blocks[index].signature == 5):
			tempX=blocks[index].x
			tempY=blocks[index].y
			temparea=blocks[index].height*blocks[index].width
		if (index == 3) and (blocks[index].signature == 5):
			if (blocks[index].y > tempY):
				chestY=blocks[index].y
				chestX=blocks[index].x
				chestarea=blocks[index].height*blocks[index].width
				HeadY=tempY
				Headarea=temparea
				tempY=0
			else:
				chestY=tempY
				chestX=tempX
				HeadY=blocks[index].y
				tempY=0
#						

except (KeyboardInterrupt):
   api.ServoShutdown()
   sys.exit()
