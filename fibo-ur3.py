import numpy
import socket
import time
import math
# import cv2

HOST = "192.168.1.51"
PORT = 30002

count = 0
home = "movej(["+str(math.radians(0))+","+str(math.radians(-90))+","+str(math.radians(0))+","+str(math.radians(-90))+","+str(math.radians(0))+","+str(math.radians(0))+"], a=1.0, v=0.5)"
p1 = "movej(["+str(math.radians(6.21))+","+str(math.radians(-122.02))+","+str(math.radians(-22.10))+","+str(math.radians(-121.38))+","+str(math.radians(90.09))+","+str(math.radians(50.65))+"], a=1.0, v=1)"
p2 = "movej(["+str(math.radians(6.10))+","+str(math.radians(-114.05))+","+str(math.radians(-84.34))+","+str(math.radians(-67.12))+","+str(math.radians(90.21))+","+str(math.radians(50.80))+"], a=1.0, v=1)"

x = 31
y = 289
cx = 0.095+(x-31)*(-0.045/383)
cy = -0.04+(y-289)*(0.215/-252)
move_xy = "movel(pose_trans(get_forward_kin(), p["+str(cx)+","+str(cy)+",0,0,0,0]), a=1.0, v=1)"
push_down = "movel(pose_trans(get_forward_kin(), p[0,0,0.05,0,0,0]), a=1.0, v=1)"

print(p1)
while (count < 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    time.sleep(0.5)

    s.send(("set_digital_out(1,True)"+"\n").encode('utf8'))
    time.sleep(0.1)
    s.send(("set_digital_out(2,True)"+"\n").encode('utf8'))
    time.sleep(2)
    # s.send((home+"\n").encode('utf8'))
    # time.sleep(5)
    # s.send((p1+"\n").encode('utf8'))
    # time.sleep(3)
    s.send((p2+"\n").encode('utf8'))
    time.sleep(3)
    s.send((move_xy+"\n").encode('utf8'))
    time.sleep(5)

    # s.send((move_x+"\n").encode('utf8'))
    # time.sleep(5)

    s.send(("set_digital_out(1,False)"+"\n").encode('utf8'))
    time.sleep(0.1)
    s.send(("set_digital_out(2,False)"+"\n").encode('utf8'))
    time.sleep(0.1)
    count = count + 1
    print(count)

    time.sleep(1)
    data = s.recv(1024)
    s.close()
    print("Received", repr(data))
