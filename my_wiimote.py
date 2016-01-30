################################################
## my_wiimote.py
################################################
## Bluetooth remote control for Raspberry Pi 
##  GPIO
################################################
## Nate Rogers
## n8_31@yahoo.com
## Last Modified May 27, 2013
################################################

import cwiid
import RPi.GPIO as io
import time
import os

# Function to control the Wii Rumble
def Rumble(x, t):
    t *= 1.0
    for i in range(x):
        wm.rumble = True
        time.sleep(t)
        wm.rumble = False
        time.sleep(0.2)

###########################################
# Functions to call the GPIO controller
###########################################
def _stop(motor):
    controller(motor,[False,False])

def _forward(motor):
    controller(motor,[True,False])

def _backward(motor):
    controller(motor,[False,True])

# Function to control the Wii LEDs
def LED(x):
    wm.led = x

def stop():
    _stop(motor1)
    _stop(motor2)
    
def end():
    stop()
    Rumble(2,0.2)
    os.system('sudo python /etc/robo-listen.py &')
    exit()
    
def forward():
    _forward(motor1)
    _forward(motor2)
    
def back():
    _backward(motor1)
    _backward(motor2)

def left():
    _forward(motor2)
    _backward(motor1)

def right():
    _forward(motor1)
    _backward(motor2)

# Call Wii Control Picker
def pick():
    stop()
    picker()
    
############################################
# Main Function to control the GPIO outputs
############################################
def controller(motor, power):
    if not len(motor)==len(power):
        print "Error!"
    else:
        for x in range(0,len(motor)):
            io.output(motor[x],power[x])

# Actions to called by Wii Controller 
actions = {0 : stop, 256 : back, 512: forward, 1024: right, 2048 : left, 7 : pick, 128 : end}

# Menu to select Wii Controls
def picker():
    print dir(wm)
    #print 'Select Mode: 1 = Keypad, 2 = Accelerometer'
    LED(15)
    Rumble(1,1.0)
    while True:
        b = wm.state['buttons']
        if b == 2:
            Rumble(1,0.5)
            LED(1)
            keypad()
        elif b == 1:
            Rumble(2,0.5)
            LED(2)
            accelerometer()

# Accelerometer Controls
def accelerometer():
    action = 0
    action1 = 3
    while True:
        s = wm.state['acc']
        b = wm.state['buttons']
        if s[0] > 140:
            action = 512 #Forward
        elif s[0] < 120:
            action = 256 #Back
        else:
            if s[1] < 120:
                action = 1024 #Right
            elif s[1] > 140:
                action = 2048 #Left
            else:
                action = 0 #Stop
        if not b == 0:
            action = b
        if not action == action1:
            try:
                actions[action]()
            except Exception, e:
                log = "Unrecognized Button Combination (" + str(e) + ")"
            action1 = action

# Keypad Controls
def keypad():
    action = 0
    action1 = 3
    while True:
        action = wm.state['buttons']
        if not action == action1:
            try:
                actions[action]()
            except Exception, e:
                log = "Unrecognized Button Combination (" + str(e) + ")"
		
        action1 = action


    

### Initiallize GPIO
io.setmode(io.BCM)
log = '' #open('/var/log/wii_pi.log','w')

motor1 = [25,22]
motor2 = [23,24]
button1 = 4
#button2 = 17

io.setup(motor1[0], io.OUT)
io.setup(motor1[1], io.OUT)
io.setup(motor2[0], io.OUT)
io.setup(motor2[1], io.OUT)
io.setup(button1, io.IN)
#io.setup(button2, io.IN)

### Initialize Wii Connection
#log.write('Press button 1 + 2 on your Wii Remote...\n')

#print dir(cwiid)

while True:
    try:
        wm=cwiid.Wiimote()
        wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        #log.write('Wii Remote connected...\n')
        picker()
        break
    except Exception, e:
        #log.write('Error Connecting to Wiimote (' + str(e) + ')...Trying Again\n')
        time.sleep(2)
