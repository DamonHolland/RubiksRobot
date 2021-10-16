import cv2 as cv
import numpy as np

frameWidth = 720
frameHeight = 720
cap = cv.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

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


while True:
    ret, img = cap.read()

    grayImage = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gausImage = cv.GaussianBlur(grayImage, (5, 5), 50, 50)
    cannyImage = cv.Canny(gausImage, 40, 120, 3)

    kernel = np.ones((5, 5), np.uint8)

    dilationImage = cv.dilate(cannyImage, kernel, iterations=1)

    h, w = dilationImage.shape

    imageCorners = [
        [(0, 0), (w, 0)],
        [(w, 0), (w, h)],
        [(w, h), (0, h)],
        [(0, h), (0, 0)]
    ]

    newDilationImage = dilationImage.copy()

    for i in range(len(imageCorners)):
        currentVect = imageCorners[i]
        newDilationImage = cv.line(newDilationImage, currentVect[0], currentVect[1], (255, 255, 255), 200)

    floodFillImage = newDilationImage.copy()

    mask = np.zeros((h + 2, w + 2), np.uint8)

    for x in range(150, 250):
        for y in range(150, 250):
            cv.floodFill(floodFillImage, mask, (x, y), 255)
            cv.floodFill(floodFillImage, mask, (w - x, y), 255)
            cv.floodFill(floodFillImage, mask, (x, h - y), 255)
            cv.floodFill(floodFillImage, mask, (w - x, h - y), 255)

    newFillImage = cv.Canny(floodFillImage, 40, 120, 3)

    frameStack = stackFrames(0.4, ([img, grayImage, gausImage],
                                   [cannyImage, dilationImage, newDilationImage],
                                   [floodFillImage, newFillImage, img]))

    cv.imshow('Rubiks Cube Viewer', frameStack)

    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()