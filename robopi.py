import RPi.GPIO as io
import time
io.setmode(io.BCM)

motor1 = [4, 17]
motor2 = [23, 24]

io.setup(motor1[0], io.OUT)
io.setup(motor1[1], io.OUT)
io.setup(motor2[0], io.OUT)
io.setup(motor2[1], io.OUT)

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
    
def go_right(args):
    _right()
    if len(args) > 1:
        #print "Sleeping..."
        time.sleep(args[1])
	_stop()

def go_left(args):
    _left()
    if len(args) > 1:
        #print "Sleeping..."
        time.sleep(args[1])
	_stop()

def go_forward(args):
    _forward()
    if len(args) > 1:
        #print "Sleeping..."
        time.sleep(args[1])
	_stop()

def go_backward(args):
    _backward()
    if len(args) > 1:
        #print "Sleeping..."
        time.sleep(args[1])
	_stop()

def go_stop(args):
    #print "Stop"
    stop(motor1)
    stop(motor2)
    if len(args) > 1:
        #print "Sleeping..."
        time.sleep(args[1])
	_stop()

def _stop():
    stop(motor1)
    stop(motor2)

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

def validate_input(x):
    instructions = ['f','b','s','l','r','q']
    max_duration = 9
    min_duration = 1
    if len(x) >= 1:
        i = 0
        while i < len(x):
            if is_even(i): 
                # Then it's an instruction
                try:
                    instructions.index(x[i])
                except:
                    break
                    return False
            else:
                # Then it's a duration
                if not x[i].isdigit():
                    return False
                else:
                    if int(x[i]) > max_duration or int(x[i]) < min_duration:
                        return False
            i += 1
        else:
            return True
    else:
        return False

def is_even(x): # x = integer
    if x % 2 == 0:
        return True
    else:
        return False

def execute_input(x):
    x = x.lower()
    if not is_even(len(x)):
        x += '0'
        #print x
    i = 0
    while i < len(x):
        if int(x[i+1]) == 0:
            instruct(x[i])
        else:
            instruct(x[i],int(x[i+1]))
        
        i += 2
        
def instruct(*args):
    if args[0] == 'f':
        go_forward(args)
    elif args[0] == 'b':
        go_backward(args)
    elif args[0] == 'l':
        go_left(args)
    elif args[0] == 'r':
        go_right(args)
    elif args[0] == 's':
        go_stop(args)
            
while True:
    x = raw_input("Input Instruction: ")
    if validate_input(x):
        if x != 'q':
            execute_input(x)
        else:
            exit()
    else:
        print "Invalid Input: Please use the pattern InstructionDurationInstructionDuration"
