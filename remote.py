import socket
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)  #Set Pin Mode according Pin Names

#-----------------------------------------------------------------------------
# GPIO Pins SETUP

motor1 = [25, 22]
motor2 = [23, 24]

GPIO.setup(motor1[0], GPIO.OUT)   
GPIO.setup(motor1[1], GPIO.OUT)    	
GPIO.setup(motor2[0], GPIO.OUT)   
GPIO.setup(motor2[1], GPIO.OUT)   

#-----------------------------------------------------------------------------

#Functions

def _left():
    #print "Left"
    forward(motor2)
    backward(motor1)

def _right(): 
    #print "Right"
    forward(motor1)
    backward(motor2)

def _forward():
    #print "Forward"
    forward(motor1)
    forward(motor2)

def _backward():
    #print "Backward"
    backward(motor1)
    backward(motor2)

def stop():
    controller(motor1,[False,False])
    controller(motor2,[False,False])
    
def forward(motor):
    #stop()
    controller(motor,[True,False])

def backward(motor):
    #stop()
    controller(motor,[False,True])
    
def controller(motor, power):
    if not len(motor)==len(power):
        print "Error!"
    else:
        for x in range(0,len(motor)):
            GPIO.output(motor[x],power[x])

#-----------------------------------------------------------------------------

RxSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
TxSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

IP = '0.0.0.0'
InPort = 7777
OutPort = 7777
TurnTime = .3

RxSock.bind((IP,InPort))

while True:
    data = RxSock.recvfrom(512)
    message = data[0]
    senderinfo = data[1]
    senderIP = senderinfo[0]
#	print "message received: ", message
#	print "message length: ", len(message)
#	print "sender's IP: ", senderIP
	
#-----------------------------------------------------------------------------

	# Handle Messages for Shutdown & Reboot	

    if (message == 'Reboot'):
        print "Rebooting System"
        TxSock.sendto('Rebooting System...',(senderIP,OutPort))

        os.system('reboot')

    if (message == 'Shutdown'):
        print "Shutting System Down Now..."
        TxSock.sendto('Shutting System Down...',(senderIP,OutPort))

        os.system('sudo shutdown now -h')

    if message == 'Quit':
        exit()
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------

    # Handle Messages for GPIO Pins	
    if message == 'forward':
        _forward()
    
    if message == 'back':
        _backward()
    
    if message == 'left':
        _left()
    
    if message == 'right':
        _right()
        
    if message == 'stop':
        stop()

    if message == 'rightup':
        stop()
        _right()
        time.sleep(TurnTime)
        _forward()
        
    if message == 'leftup':
        stop()
        _left()
        time.sleep(TurnTime)
        _forward()
    
    if message == 'rightback':
        stop()
        _left()
       	time.sleep(TurnTime)
        _backward()
    
    if message == 'leftback':
        stop()
        _right()
        time.sleep(TurnTime)
        _backward()
        
    if message == 'dance':
        for x in range(1,5):
            _right()
            time.sleep(.5)
            _left()
            time.sleep(.5)
        stop()
		#PIN 3
	#if (message == 'P3H'):
	#	print "Pin 3 is now High"
	#	GPIO.output(3, True)
	#	TxSock.sendto('Pin 3 is now High',(senderIP,OutPort))

	#elif (message == 'P3L'):
 	#	print "Pin 3 is now Low"
	#	GPIO.output(3, False)
	#	TxSock.sendto('Pin 3 is now Low',(senderIP,OutPort))

		
#-----------------------------------------------------------------------------
