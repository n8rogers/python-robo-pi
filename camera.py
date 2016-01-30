import os

folder = "/home/pi/stills"
filetype = '.jpg'
rotation = '180'
filename = 'test'
pics = 4
start = 0

#print '/opt/vc/bin/raspistill ' + output[0] + output[1]
for x in range(start,pics):
    output = filename + str(x) + filetype
    os.system('/opt/vc/bin/raspistill -o ' + folder + '/' + output + ' -rot ' + rotation)