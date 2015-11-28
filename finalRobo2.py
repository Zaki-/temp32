import sys

#appends api directory path to sys path
#sys.path.append("/home/pi/Human_Robots_Interaction_Fall15")
sys.path.append("/home/pi/HROS1-Framework/Linux/project/Human_Robots_Interaction_Fall15")


import api 
import sys

from pixy import *
from ctypes import *

tempY=0
speedInc=0
timer = 0
chestX = 0
chestY=300
HeadY=300
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
		api.PlayAction(1)
		walkFlag = False



def Sit(b):#pass true to make the robot sit
	global sitFlag
	if (b == True) and (sitFlag == False):
		api.PlayAction(16)
		sitFlag = True
	elif (b == False) and (sitFlag ==True):
		api.PlayAction(1)
		sitFlag = False
		

def SoS():
	if (sitFlag == False) and (walkFlag == False):
		print 'api.PlayAction(sos)'

def UVA():
	if (sitFlag == False) and(walkFlag == False):
		print 'api.PlayAction(UVA)'

def checkSign(LHX,RHX,LHY,RHY,HeadY,chestX,chestY):
	HY=abs(LHY-RHY)
	rateY=abs(HeadY-chestY)
	# stand up
	if (abs(LHY-RHY-chestY)<10):
		WalkReady(False)
		sit(False) #stand
	# sit down
	if (HY<10) and (abs(chestY-HY)-abs(int(0.5*rateY))<10) and (HY < chestY) and (HY < HeadY):
	#the distance between chestY and both hands Y(HY) almost equels half of distance between head and chest
		WalkReady(False)
		sit(True)
	# start walking
	if (HY<10) and (abs(headY-HY)-abs(int(0.5*rateY))<10) and (HY<HeadY) and (HY > chestY):
	# the distance between head and both hands Y almost equels half of  the distance between the head and chest 
		WalkReady(True)


	# UVA
	if (HY<10) and (RHX == LHX) and (HY > chestY):
		UVA()
	# SoS
	if (HY<10) and (abs(headY-HY)-abs(int(0.5*rateY))<10) and (HY>HeadY) and (HY > chestY):
		SoS()



sit = 0
walk = False
X=0  # 0 - 320
color = 'red'


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
api.SetMotorValue(20,433)
try:
  while 1:
     count = pixy_get_blocks(100, blocks)
     if (int(api.BatteryVoltLevel()) <= battryLim):
      if (int(api.BatteryVoltLevel()) <= battryLim):
       if (int(api.BatteryVoltLevel()) <= battryLim):

	print 'Low Battery'
	api.Walk(False)
	api.PlayAction(15)
	api.ServoShutdown()
	sys.exit()
     else:
#       print 'Battery power', int(api.BatteryVoltLevel())
       if count > 0:
#	 print 'count' , count
	 #print 'block' , blocks
         #blocks found
	 Uframe=frame/500
         print 'frame %3d:' % (Uframe)
         frame = frame +1
         for index in range(0, count):
		# pixy reselution 320X200	     
#             	print '[Block_type=%d  Sig=%d  X=%3d  Y=%3d   W=%3d   H=%3d]' % (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y, blocks[index].width, blocks[index].height)
             	if ((blocks[index].signature == 1) and (chestX != 0)):# or (blocks[index].signature == 1)):
             		if (blocks[index].x > chestX):
				LHX=centerX(blocks[index].x)
				LHY=centerY(blocks[index].y)
			elif (blocks[index].x <= chestX):
				RHX=centerX(blocks[index].x)
				RHY=centerY(blocks[index].y)
		
             	if (blocks[index].signature == 5):
			chestX=centerX(blocks[index].x)
			chestY=centerY(blocks[index].y)
			if (HeadY ==300): HeadY=chestY
			if (chestY == 300): chestY=tempY
			if HeadY < chestY :
				tempY=chestY
				chestY=HeadY
				HeadY=tempY
				
			elif HeadY >= tempY :
				
				chestY = tempY
			
		checkSign(LHX,RHX,LHY,RHY,HeadY,chestX,chestY)
		print 'LHY=%d chestY=%d HeadY=%d RHY=%d' %(LHY, chestY, HeadY, RHY)
#		SetHead(chestX,chestY)
#		print 'RHX=%d RHY=%d CX=%d CY=%d LHX=%d LHY=%d' % (RHX, RHY, chestX, chestY, LHX, LHY)
#		speedInc = 0
#		timer = 0
#	     	if (((blocks[index].signature == 5) or (blocks[index].signature == 5)):# and (walk == True)):
#			print 'track'
#			X = centerX(blocks[index].x)
#			print 'X track', X
#			RoboTurn(Y)	 

    		#call the walk function
#	     	RoboWalk(color, X)
except (KeyboardInterrupt):
   api.ServoShutdown()
   sys.exit()
