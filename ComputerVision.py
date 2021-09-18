import cv2 as cv
import numpy as np

vid = cv.VideoCapture(0)

if not vid.isOpened():
    print("plug in your camera lmao")
    exit()

while True:
    ret, frame = vid.read()

    if not ret:
        print("where the frames at?")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break

vid.release()
cv.destroyAllWindows()