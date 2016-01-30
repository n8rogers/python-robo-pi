import RPi.GPIO as io
import time
import os

button1 = 4

io.setmode(io.BCM)
io.setup(button1, io.IN)

#print 'Ready for input...'
while True:
    if io.input(button1) == False:
        os.system('sudo python /etc/my_wiimote.py &')
        exit()
    time.sleep(0.1)