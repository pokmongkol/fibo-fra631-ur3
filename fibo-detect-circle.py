import cv2
import numpy as np

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
        cv2.putText(roi, str(x)+","+str(y), (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)
        # DRAW CIRCLE TO CONTOUR
        ellipse = cv2.fitEllipse(cnt)
        cv2.ellipse(roi, ellipse, (0, 255, 0), 2)
        counter+=1

    cv2.putText(roi, str(counter), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,0,0), 2, cv2.LINE_AA)
    cv2.imshow("FIBO - FRA631 Class Project 2022", roi)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()