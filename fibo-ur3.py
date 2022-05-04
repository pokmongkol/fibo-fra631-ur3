import socket
import time
import math

HOST = "192.168.1.51"
PORT = 30002

count = 0
home = "movej(["+str(math.radians(0))+","+str(math.radians(-90))+","+str(math.radians(0))+","+str(math.radians(-90))+","+str(math.radians(0))+","+str(math.radians(0))+"], a=1.0, v=0.5)"
p1 = "movej(["+str(math.radians(5.83))+","+str(math.radians(-121.11))+","+str(math.radians(-23.77))+","+str(math.radians(-122.80))+","+str(math.radians(90.66))+","+str(math.radians(50.14))+"], a=1.0, v=1)"
p2 = "movej(["+str(math.radians(0.06))+","+str(math.radians(-101.28))+","+str(math.radians(-102.76))+","+str(math.radians(-64.08))+","+str(math.radians(91.77))+","+str(math.radians(176.95))+"], a=1.0, v=1)"
p3 = "movel(["+str(math.radians(5.83))+","+str(math.radians(-121.11))+","+str(math.radians(-23.77))+","+str(math.radians(-122.80))+","+str(math.radians(90.66))+","+str(math.radians(50.14))+"], a=1.0, v=1)"

x = 277
y = 163
cx = 0+(x-97)*(0.165/346)
cy = 0+(y-2)*(0.135/287)
print(cx)
print(cy)
move_xy = "movel(pose_trans(get_forward_kin(), p["+str(cx)+","+str(cy)+",0,0,0,0]), a=1.0, v=1)"
push_down = "movel(pose_trans(get_forward_kin(), p[0,0,0.07,0,0,0]), a=1.0, v=1)"
push_up = "movel(pose_trans(get_forward_kin(), p[0,0,-0.07,0,0,0]), a=1.0, v=1)"

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
    s.send((p1+"\n").encode('utf8'))
    time.sleep(4)

    s.send((p2+"\n").encode('utf8'))
    time.sleep(4)
    s.send((move_xy+"\n").encode('utf8'))
    time.sleep(3)
    s.send((push_down+"\n").encode('utf8'))
    time.sleep(5)
    s.send((push_up+"\n").encode('utf8'))
    time.sleep(3)

    s.send((p3+"\n").encode('utf8'))
    time.sleep(4)

    s.send(("set_digital_out(1,False)"+"\n").encode('utf8'))
    time.sleep(0.1)
    s.send(("set_digital_out(2,False)"+"\n").encode('utf8'))
    time.sleep(0.1)
    count = count + 1

    time.sleep(1)
    data = s.recv(1024)
    s.close()
    print("Received", repr(data))
