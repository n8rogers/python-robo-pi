#Test Input for GPIO

import RPi.GPIO as io
import time

button1 = 4
button2 = 17

io.setmode(io.BCM)
io.setup(button1, io.IN)
io.setup(button2, io.IN)

print 'Ready for input...'
while True:
    if io.input(button1) == False:
        print 'Button 1 was pressed'
    if io.input(button2) == False:
        print 'Button 2 was pressed'
    time.sleep(0.1)
