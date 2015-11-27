#!/usr/bin/python3
import sys

#appends api directory path to sys path
#sys.path.append("/home/pi/Human_Robots_Interaction_Fall15")
sys.path.append("/home/pi/HROS1-Framework/Linux/project/Human_Robots_Interaction_Fall15")


#!/usr/bin/python
import pyaudio
import audioop
import wave

import api
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


def RoboWalk(speed):
	global walk
	print 'Robo walking'
	api.Walk(True)
	api.WalkMove(speed)
	walk = True
# End of RoboWalk

def RoboStop():
	global walk
	print 'Robo stop and sitting'
	api.Walk(False)
	api.PlayAction(16)
	walk = False
# End of RoboStop

RoboInit()

rmsMAX =0
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
THRESHOLD = 250
walk = False
# vars for morse 
ii=0	#index to check morse code-- counter for rms greater than threshold
	#index for array code[]
jj=19	#index to find the reset and space

code=[]		#store dots, dashes and spaces
words=[]
print 'coede = = = = ', code[:]
finalWord=[]
# functions for morse

def DotDashCheck(index, th):
	global kk, code
	if ((index < th) and (index > 0)):
		print kk
		code[7]='0'
		kk=kk+1
	elif (index >= th):
		code[kk]='1'
		kk=kk+1


def ResetSpaceCheck(index, th):
	global kk, code
	if ((index < th) and (index > 0)):
		print kk
		code[kk]='s'
	elif (index >= th):
		kk=0
		code[:]=[]

def CodeCheck(code):
	global words
	ii=0
	temp=['s','s','s','s']
	for w in code[:]:
		if ((w == '.') or (w == '-')):
			if (ii < 4):
				temp[ii]=w
				ii+=1
			
			else:
				temp=['s','s','s','s']
				print 'wrong code !!'
			
		elif (w == 's'):
		        if (ii == 0):
		        	temp=['s','s','s','s']
			ii=0
			print 'temp=', temp
			words.append(Morse2Eng(temp))
		else:
			temp=['s','s','s','s']
			print 'wrong code !'

def Morse2Eng(code):
	if (code[:]==['.','.','.','s']):return 'S'
	elif (code[:]==['-','-','-','s']):return 'O'
	elif (code[:]==['.','-','-','s']):return 'W'
	elif (code[:]==['-','-','s','s']):return 'M'
	elif (code[:]==['.','.','-','s']):return 'U'
	elif (code[:]==['.','.','.','-']):return 'V'
	elif (code[:]==['.','-','s','s']):return 'A'
	elif (code[:]==['.','-','.','-']):return 'A'
	else: return 0

Word=[]
def Add2Word(code):
	global Word
	if (code[:]==['.','.','.']):       Word.append('S')
	elif (code[:]==['-','-','-']):     Word.append('O')
	elif (code[:]==['.','-','-']):     Word.append('W')
	elif (code[:]==['-','-']):         Word.append('M')
	elif (code[:]==['.','.','-']):     Word.append('U')
	elif (code[:]==['.','.','.','-']): Word.append('V')
	elif (code[:]==['.','-']):         Word.append('A')
	elif (code[:]==['.','-','.','.']): Word.append('L')
	elif (code[:]==['-','.','-']):     Word.append('K')
	elif (code[:]==['-']):             Word.append('T')
	elif (code[:]==['.','-','-','.']): Word.append('P')
	
def RoboCommand(words):
	global command
	strg='' 
	for w in words[:]:
	     if (w !=0):
		strg=strg+str(w)
	if (strg == 'W'):print 'api.PlayAction(W )'
	elif (strg == 'M'):print 'api.PlayAction(M )'
	elif (strg == 'SOS'):print 'api.PlayAction(SOS )'
	elif (strg == 'UVA'):print 'api.PlayAction(UVA )'


p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
	dev = p.get_device_info_by_index(i)
	print((i, dev['name'],dev['maxInputChannels']))

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
		input_device_index = 2,
                frames_per_buffer=CHUNK)
codeFlag = False
print("* recording")
try:
 while True:
    try:
    	data = stream.read(CHUNK)
    except IOError as ex:
	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = 2,
                frames_per_buffer=CHUNK)
	
	data = stream.read(CHUNK)
	
    rms = audioop.rms(data, 2)
    if (rms > rmsMAX):
	rmsMAX = rms

#	main check

    if(rms>THRESHOLD):

#	print (rms), (rmsMAX)
#	ResetSpaceCheck(jj, 4)
	ii=ii+1
	if (ii == 1):
		code.append('.')
	elif (ii == 5):
		code.pop()
		code.append('-')
	jj=0
	print 'code= ', code[:]
	
    else:
#	print 0 , (rmsMAX)	  
#	DotDashCheck(ii, 7)
#	space devided into:
#	1- space between codes within the letter ex ...=S ..-=U
#	2- space between letters ex ... --- ... = S O S
#	3- long space is reset
	#add space between letters
#       if (code[:] != []):	
	if (jj == 8):
		#code.append('s')
		Add2Word(code)
		code=[]
	if (jj == 20):#reset
		#need to copy code to command[]before we lose the data
		#or send the code for execution 
		#if (code[:] != []):code.pop() # 's'
		print 'final code=', code[:]
		Add2Word(code)
		#CodeCheck(code)
		#send command to the robot
		RoboCommand(Word)
		if (Word != []):
			finalWord=Word
		print 'final word=',finalWord[:]
		Word=[]
		code=[]
	print 'finalwords = ' ,finalWord[:]	
	jj=jj+1  
	ii=0
	

except (KeyboardInterrupt):
	print 'stoped by user ...'
	stream.stop_stream()
	stream.close()
	p.terminate()
	api.ServoShutdown()
	sys.exit()

stream.stop_stream()
stream.close()
p.terminate()

