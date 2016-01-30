import RPi.GPIO as io
import time
io.setmode(io.BCM)

motor1 = [4, 17]
motor2 = [23, 24]

io.setup(motor1[0], io.OUT)
io.setup(motor1[1], io.OUT)
io.setup(motor2[0], io.OUT)
io.setup(motor2[1], io.OUT)

def spin(direction,duration,action):
    direction = direction.lower()
    if direction == 'l':
        turn_left()
    elif direction == 'r':
	turn_right()
    else:
	print "Error"
	stop()
    time.sleep(duration)
    if action == 's':
	stop()
    elif action == 'f':
	go_forward()
    elif action == 'b':
        go_backward()
    else:
	print 'Error'
	stop()

def turn_left():
    forward(motor2)
    backward(motor1)
def turn_right(): 
    forward(motor1)
    backward(motor2)

def go_forward():
    forward(motor1)
    forward(motor2)

#def go_forward(duration):
#    go_forward()
#    time.sleep(duration)
#    stop()

def go_backward():
    backward(motor1)
    backward(motor2)

#def go_backward(duration):
#    go_backward()
#    time.sleep(duration)
#    stop()

def stop(motor):
    controller(motor,[False,False])
    
def forward(motor):
    controller(motor,[True,False])

def backward(motor):
    controller(motor,[False,True])
    
def controller(motor, power):
    if not len(motor)==len(power):
        print "Error!"
    else:
        for x in range(0,len(motor)):
            io.output(motor[x],power[x])
            #print motor[x], " ", power[x]

while True:
    x = raw_input("Input Instruction: ")
    if x == 'r':
        spin(x,.5,'f')
    elif x == 'l':
        spin(x,.5,'f')
    elif x == 'f':
        go_forward()
    elif x == 's':
        stop(motor1)
        stop(motor2)
    elif x == 'b':
        go_backward()
    elif x == 'q':
	stop(motor1)
	stop(motor2)
        break
    else:
        print "Invalid Input!"
