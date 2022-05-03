import numpy
import socket
import time
import math
# import cv2

HOST = "192.168.1.51"
PORT = 30002

count = 0
home = "movej(["+str(math.radians(0))+","+str(math.radians(-90))+","+str(math.radians(0))+","+str(math.radians(-90))+","+str(math.radians(0))+","+str(math.radians(0))+"], a=1.0, v=0.5)"
command0 = "movej(["+str(math.radians(2.68))+","+str(math.radians(-89.39))+","+str(math.radians(-91.44))+","+str(math.radians(-85.94))+","+str(math.radians(87.86))+","+str(math.radians(-25.47))+"], a=1.0, v=1)"
command11 = "movej(["+str(math.radians(5.02))+","+str(math.radians(-175.87))+","+str(math.radians(-0.5))+","+str(math.radians(-93.03))+","+str(math.radians(90.36))+","+str(math.radians(-24.07))+"], a=1.0, v=1.5)"
command12 = "movej(["+str(math.radians(24.06))+","+str(math.radians(-166.27))+","+str(math.radians(-20.97))+","+str(math.radians(-82.15))+","+str(math.radians(90.17))+","+str(math.radians(-4.97))+"], a=1.0, v=1.5)"
command2 = "movel(pose_trans(get_forward_kin(), p[0,0,0.05,0,0,0]), a=1.0, v=1)"

print(command0)
while (count < 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    time.sleep(0.5)

    s.send(("set_digital_out(1,True)"+"\n").encode('utf8'))
    time.sleep(0.1)
    s.send(("set_digital_out(2,True)"+"\n").encode('utf8'))
    time.sleep(2)
    s.send((home+"\n").encode('utf8'))
    time.sleep(5)
    s.send((command0+"\n").encode('utf8'))
    time.sleep(3)
    s.send((command11+"\n").encode('utf8'))
    time.sleep(3)
    s.send((command2+"\n").encode('utf8'))
    time.sleep(5)
    s.send((command11+"\n").encode('utf8'))
    time.sleep(3)
    s.send((command0+"\n").encode('utf8'))
    time.sleep(5)

    s.send((command12+"\n").encode('utf8'))
    time.sleep(3)
    s.send((command2+"\n").encode('utf8'))
    time.sleep(5)
    s.send((command12+"\n").encode('utf8'))
    time.sleep(3)
    s.send((command0+"\n").encode('utf8'))
    time.sleep(3)

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
