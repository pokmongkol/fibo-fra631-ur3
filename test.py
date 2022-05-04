import socket
import time

HOST = "192.168.1.51"
PORT = 30002

count = 0

while (count < 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    time.sleep(0.5)

    s.send(("set_digital_out(1,True)"+"\n").encode('utf8'))
    time.sleep(0.1)
    s.send(("set_digital_out(2,True)"+"\n").encode('utf8'))
    time.sleep(0.1)

    s.send(("get_actual_joint_positions()"+"\n").encode('utf8'))
    time.sleep(0.1)
    msg = s.recv(1024)
    print(msg)

    s.send(("get_analog_in(0)"+"\n").encode('utf8'))
    time.sleep(0.1)
    msg = s.recv(1024)
    print(msg)

    s.send(("set_digital_out(1,False)"+"\n").encode('utf8'))
    time.sleep(0.1)
    s.send(("set_digital_out(2,False)"+"\n").encode('utf8'))
    time.sleep(0.1)
    count = count + 1

    time.sleep(1)
    s.close()
