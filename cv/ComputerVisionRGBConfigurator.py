import cv2 as cv2
import numpy as np
import ComputerVisionRubiksRGB


def mouseRGB(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colorsB = frame[y,x,0]
        colorsG = frame[y,x,1]
        colorsR = frame[y,x,2]
        colors = frame[y,x]
        print("Red: ",colorsR)
        print("Green: ",colorsG)
        print("Blue: ",colorsB)
        print("BRG Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)

        print("PIXEL CENTER")
        print(ComputerVisionRubiksRGB.RGBUint8.identifyBGR(frame, x, y))


cv2.namedWindow('mouseRGB')
cv2.setMouseCallback('mouseRGB',mouseRGB)

capture = cv2.VideoCapture(1)

while(True):

    ret, frame = capture.read()

    cv2.imshow('mouseRGB', frame)

    if cv2.waitKey(1) == 'q':
        break

capture.release()
cv2.destroyAllWindows()
