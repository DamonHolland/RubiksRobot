import cv2 as cv
import numpy as np

# CONFIG
NUM_POINTS = 4
IMAGE_NAME = "FacePic.jpg.jpg"


def empty(a):
    pass


def stackFrames(scale, frameArray):
    rows = len(frameArray)
    cols = len(frameArray[0])
    rowsAvailable = isinstance(frameArray[0], list)
    width = frameArray[0][0].shape[1]
    height = frameArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if frameArray[x][y].shape[:2] == frameArray[0][0].shape[:2]:
                    frameArray[x][y] = cv.resize(frameArray[x][y], (0, 0), None, scale, scale)
                else:
                    frameArray[x][y] = cv.resize(frameArray[x][y],
                                                 (frameArray[0][0].shape[1], frameArray[0][0].shape[0]), None, scale,
                                                 scale)
                if len(frameArray[x][y].shape) == 2: frameArray[x][y] = cv.cvtColor(frameArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(frameArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if frameArray[x].shape[:2] == frameArray[0].shape[:2]:
                frameArray[x] = cv.resize(frameArray[x], (0, 0), None, scale, scale)
            else:
                frameArray[x] = cv.resize(frameArray[x], (frameArray[0].shape[1], frameArray[0].shape[0]), None, scale,
                                          scale)
            if len(frameArray[x].shape) == 2: frameArray[x] = cv.cvtColor(frameArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(frameArray)
        ver = hor

    return ver


def getContours(frame, frameContour):
    contours, hierarchy = cv.findContours(frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    if contours:
        maxContour = contours[0]
        maxArea = cv.contourArea(maxContour)

        for cnt in contours:
            area = cv.contourArea(cnt)
            maxArea = cv.contourArea(maxContour)

            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)

            if len(approx) == 6 and maxArea < area:
                maxContour = cnt

        if maxArea > 10000:
            cv.drawContours(frameContour, maxContour, -1, (255, 0, 255), 7)
            peri = cv.arcLength(maxContour, True)
            approx = cv.approxPolyDP(maxContour, 0.02 * peri, True)
            x, y, w, h = cv.boundingRect(approx)
            cv.rectangle(frameContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
            cv.putText(frameContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv.FONT_HERSHEY_COMPLEX, .7,
                       (0, 255, 0), 2)
            cv.putText(frameContour, "Area: " + str(int(maxArea)), (x + w + 20, y + 45), cv.FONT_HERSHEY_COMPLEX, .7,
                       (0, 255, 0), 2)

            return approx


def drawPoints(pointsArry: list, frameChange):
    for x in range(len(pointsArry)):
        if x == len(pointsArry) - 1:
            start = (pointsArry[x][0][0], pointsArry[x][0][1])
            end = (pointsArry[0][0][0], pointsArry[0][0][1])
        else:
            start = (pointsArry[x][0][0], pointsArry[x][0][1])
            end = (pointsArry[x + 1][0][0], pointsArry[x + 1][0][1])

        frameChange = cv.line(frameChange, start, end, (0, 0, 255), 9)

    return frameChange


frame = cv.imread(IMAGE_NAME)

kernel = np.ones((5, 5))

frameContour = frame.copy()
frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
frameBlur = cv.GaussianBlur(frameGray, (3, 3), 50, 50)

frameCanny = cv.Canny(frameGray, 150, 80)
frameDil = cv.dilate(frameCanny, kernel, iterations=1)

points = getContours(frameDil, frameContour)

if points is not None:
    if len(points) == NUM_POINTS:
        frame = drawPoints(points, frame)

frameStack = stackFrames(0.8, ([frame, frameCanny, frameGray],
                                [frameDil, frameBlur, frameContour]))

cv.imshow('Rubiks Cube Viewer', frameStack)

cv.waitKey(0)
cv.destroyAllWindows()
