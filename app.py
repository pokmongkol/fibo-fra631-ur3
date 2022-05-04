import cv2
import numpy as np
import socket
import time
import math


def moveUR3(x, y):

    HOST = "192.168.1.51"
    PORT = 30002

    count = 0
    home = "movej(["+str(math.radians(0))+","+str(math.radians(-90))+","+str(math.radians(0))+","+str(math.radians(-90))+","+str(math.radians(0))+","+str(math.radians(0))+"], a=1.0, v=0.5)"
    p1 = "movej(["+str(math.radians(5.83))+","+str(math.radians(-121.11))+","+str(math.radians(-23.77))+","+str(math.radians(-122.80))+","+str(math.radians(90.66))+","+str(math.radians(50.14))+"], a=1.0, v=50)"
    p2 = "movej(["+str(math.radians(0.06))+","+str(math.radians(-101.28))+","+str(math.radians(-102.76))+","+str(math.radians(-64.08))+","+str(math.radians(91.77))+","+str(math.radians(176.95))+"], a=1.0, v=50)"
    p3 = "movel(["+str(math.radians(5.83))+","+str(math.radians(-121.11))+","+str(math.radians(-23.77))+","+str(math.radians(-122.80))+","+str(math.radians(90.66))+","+str(math.radians(50.14))+"], a=1.0, v=50)"

    cx = 0+(x-97)*(0.165/346)
    cy = 0+(y-2)*(0.135/287)
    print(cx)
    print(cy)
    move_xy = "movel(pose_trans(get_forward_kin(), p["+str(cx)+","+str(cy)+",0,0,0,0]), a=1.0, v=1)"
    push_down = "movel(pose_trans(get_forward_kin(), p[0,0,0.10,0,0,0]), a=1.0, v=1)"
    push_up = "movel(pose_trans(get_forward_kin(), p[0,0,-0.10,0,0,0]), a=1.0, v=1)"

    while (count < 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        time.sleep(0.5)

        s.send(("set_digital_out(1,True)"+"\n").encode('utf8'))
        time.sleep(0.1)
        s.send(("set_digital_out(2,True)"+"\n").encode('utf8'))
        time.sleep(0.5)

        # s.send((home+"\n").encode('utf8'))
        # time.sleep(5)

        s.send((p1+"\n").encode('utf8'))
        time.sleep(3)

        s.send((p2+"\n").encode('utf8'))
        time.sleep(3)

        s.send((move_xy+"\n").encode('utf8'))
        time.sleep(2)
        s.send((push_down+"\n").encode('utf8'))
        time.sleep(10)
        s.send((push_up+"\n").encode('utf8'))
        time.sleep(2)

        s.send((p3+"\n").encode('utf8'))
        time.sleep(3)

        s.send(("set_digital_out(1,False)"+"\n").encode('utf8'))
        time.sleep(0.1)
        s.send(("set_digital_out(2,False)"+"\n").encode('utf8'))
        time.sleep(0.1)
        count = count + 1

        time.sleep(1)
        data = s.recv(1024)
        s.close()
        print("Received", repr(data))

cap = cv2.VideoCapture()
cap.open(1, cv2.CAP_DSHOW)

while(cap.read()):

    ref,frame = cap.read()
    roi = frame[:1080, 0:1920]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (15,15), 0)
    thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
    kernel = np.ones((3,3), np.uint8) # [[1 1 1],[1 1 1],[1 1 1]]
    # closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 4)

    # result_img = closing.copy()
    result_img = thresh.copy()
    contours,hierachy = cv2.findContours(result_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x = 0
    y = 0
    counter = 0
    for cnt in contours:
        # FIND CIRCLE CONTOUR
        x,y,w,h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h
        if (aspect_ratio > 1.04 or aspect_ratio < 0.96):
            continue
        # FIND CIRCLE REQUIRED SIZE
        area = cv2.contourArea(cnt)
        if area < 20000 or area > 24000:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.putText(roi, "x="+str(x)+", y="+str(y), (175, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        btn = cv2.waitKey(1)
        if (btn == 32):
            moveUR3(x, y)
            cv2.destroyAllWindows()

        # DRAW CIRCLE TO CONTOUR
        ellipse = cv2.fitEllipse(cnt)
        cv2.ellipse(roi, ellipse, (0, 255, 0), 2)
        counter+=1

    cv2.putText(roi, "Found: "+str(counter), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)

    cv2.putText(roi, "pH: ", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
    cv2.putText(roi, "Base: ", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
    cv2.putText(roi, "Shoulder: ", (10, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
    cv2.putText(roi, "Elbow: ", (10, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
    cv2.putText(roi, "Wrist1: ", (10, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
    cv2.putText(roi, "Wrist2: ", (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
    cv2.putText(roi, "Wrist3: ", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
    cv2.imshow("FIBO - FRA631 Class Project 2022", roi)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break



cap.release()
cv2.destroyAllWindows()


