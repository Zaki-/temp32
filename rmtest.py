import sys
import api

from time import sleep
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
RoboInit()

# To control single servo 
def SingleMotor(ID, POS): 
#ID: servo ID - POS: the target position - TIME:the time it takes for the servo to go to the target position POS max is 5sec
  if (ID>=1) and (ID<=20) and (POS>=1) and (POS<=1024):# and (TIME>0) and (TIME<=5):
    OldPos=api.GetMotorValue(ID) #read the current servo position
#    DIS = abs(POS-OldPos) 
#    StepDelay=TIME/float(DIS)
    for i in range(OldPos,POS):
      api.SetMotorValue(ID,i)
#      sleep(StepDelay)
flag = True
#api.PlayAction(4)
#api.PlayAction(1)
#api.PlayAction(44)
#for i in range(1,21):
#	print api.GetMotorValue(i)

def move():
#	SingleMotor(1, 740)
	SingleMotor(2, 287)
#	SingleMotor(3, 361)
	SingleMotor(4, 644)
#	SingleMotor(5, 382)
	SingleMotor(6, 628)
def standupSign():#done	
	api.SetMotorValue(1,716)
	api.SetMotorValue(2,303)
	sleep(0.1)
	api.SetMotorValue(3,371)
	api.SetMotorValue(4,651)
	api.SetMotorValue(5,544)
	api.SetMotorValue(6,446)

def walkSign():#done
	api.SetMotorValue(1,723)
	api.SetMotorValue(2,313)
	api.SetMotorValue(3,371)
	api.SetMotorValue(4,651)
	api.SetMotorValue(5,317)
	api.SetMotorValue(6,705)

def uvaSign():#done
	x=api.GetMotorValue(1)
	api.SetMotorValue(1,1023)
        x=api.GetMotorValue(2)
	api.SetMotorValue(2,0)
	sleep(0.1)
	api.SetMotorValue(3,366)
	api.SetMotorValue(4,665)
	api.SetMotorValue(5,584)
	api.SetMotorValue(6,436)


def sosSign():#done
	x1=api.GetMotorValue(1)
	y1=api.GetMotorValue(2)	
        x=(857-x1)/50
        y=(171-y1)/50
        for i in range(0,50):
		x1=x1+x
		y1=y1+y
		api.SetMotorValue(1,x1)
		api.SetMotorValue(2,y1)
		sleep(0.01)
        api.SetMotorValue(1,857)
        api.SetMotorValue(2,171)
	api.SetMotorValue(3,371)
	api.SetMotorValue(4,651)
	api.SetMotorValue(5,410)
	api.SetMotorValue(6,626)

def initSign():#done
        x1=api.GetMotorValue(1)
        y1=api.GetMotorValue(2)
        x=(387-x1)/50
        y=(641-y1)/50
        for i in range(0,50):
                x1=x1+x
                y1=y1+y
                api.SetMotorValue(1,x1)
                api.SetMotorValue(2,y1)
                sleep(0.01)
	
	api.SetMotorValue(1,387)
	api.SetMotorValue(2,641)
	sleep(0.2)
	api.SetMotorValue(3,460)
	api.SetMotorValue(4,563)
	api.SetMotorValue(5,452)
	api.SetMotorValue(6,572)

#ID: 1 (R_sholder) 387
#ID: 2 (L_sholder) 641
#ID: 3 (R_shol_roll) 460
#ID: 4 (R_shol_roll) 563
#ID: 5 (R_elbow) 452
#ID: 6 (R_elbow) 572







def readMotors():

	print 'ID: 1 (R_sholder)', api.GetMotorValue(1)
	print 'ID: 2 (L_sholder)', api.GetMotorValue(2)
	print 'ID: 3 (R_shol_roll)', api.GetMotorValue(3)
	print 'ID: 4 (R_shol_roll)', api.GetMotorValue(4)
	print 'ID: 5 (R_elbow)', api.GetMotorValue(5)
	print 'ID: 6 (R_elbow)', api.GetMotorValue(6)
	print 'ID: 7 (R_hip_yaw)', api.GetMotorValue(7)
	print 'ID: 8 (R_hip_yaw)', api.GetMotorValue(8)
#def servosMove(id1,id2,)
#	for i in range(1,1024):
		
try:
    while True:
      if flag == True:
        flag = False
#	standupSign()
#	sleep(3)
#	walkSign()
#	sleep(3)
#	standupSign()
#	sleep(3)
	initSign()
	sleep(3)
#	standupSign()
#	sleep(0.2)
	sosSign()
	sleep(3)
#	standupSign()
#	sleep(0.2)
	initSign()
#	api.PlayAction(2)
	readMotors()
#	api.PlayAction(16)
#	move()
#	api.SetMotorValue(1,800)
#	api.SetMotorValue(2,233)


#def walkSign()
except (KeyboardInterrupt):
                api.ServoShutdown()
                sys.exit()	

#sys.exit()
# stand up sign
#ID: 1 (R_sholder) 684
#ID: 2 (L_sholder) 351
#ID: 3 (R_shol_roll) 367
#ID: 4 (R_shol_roll) 661
#ID: 5 (R_elbow) 489
#ID: 6 (R_elbow) 547
#ID: 7 (R_hip_yaw) 512
#ID: 8 (R_hip_yaw) 516

#page 44
#ID: 1 (R_sholder) 660
#ID: 2 (L_sholder) 381
#ID: 3 (R_shol_roll) 378
#ID: 4 (R_shol_roll) 644
#ID: 5 (R_elbow) 452
#ID: 6 (R_elbow) 572
#ID: 7 (R_hip_yaw) 510
#ID: 8 (R_hip_yaw) 510

#
#ID: 1 (R_sholder) 740
#ID: 2 (L_sholder) 287
#ID: 3 (R_shol_roll) 361
#ID: 4 (R_shol_roll) 644
#ID: 5 (R_elbow) 382
#ID: 6 (R_elbow) 628
#ID: 7 (R_hip_yaw) 513
#ID: 8 (R_hip_yaw) 516

# stand up
#ID: 1 (R_sholder) 387
#ID: 2 (L_sholder) 641
#ID: 3 (R_shol_roll) 460
#ID: 4 (R_shol_roll) 563
#ID: 5 (R_elbow) 452
#ID: 6 (R_elbow) 572

