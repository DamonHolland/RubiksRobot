import cv2 as cv
import numpy as np
import ComputerVisionRubiksRGB

# CONFIG
NUM_POINTS = 4

frameWidth = 720
frameHeight = 720
cap = cv.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

if not cap.isOpened():
    print("Camera cannot be opened. Exiting...")
    exit()


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


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1)*np.dot(d2, d2)))


def find_squares(frame):
    frame = cv.GaussianBlur(frame, (5, 5), 0)
    squares = []
    countS = 0
    for gray in cv.split(frame):
        bin = cv.Canny(gray, 500, 700, apertureSize=5)
        bin = cv.dilate(bin, None)
        for threshold in range(0, 255, 26):
            if threshold != 0:
                ret, bin = cv.threshold(gray, threshold, 255, cv.THRESH_BINARY)
            contours, _hierarchy = cv.findContours(
                bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and 60000 > cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max(
                        [angle_cos(cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4]) for i in range(4)])
                    if max_cos < 0.2 and countS < 1:
                        uniqueSquare = True

                        if uniqueSquare:
                            squares.append(cnt)
                            countS = countS + 1
    return squares


while True:
    ret, frame = cap.read()

    kernel = np.ones((5, 5))

    frameContour = frame.copy()
    frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frameBlur = cv.GaussianBlur(frameGray, (3, 3), 50, 50)

    frameCanny = cv.Canny(frameGray, 150, 80)
    frameDil = cv.dilate(frameCanny, kernel, iterations=1)

    points = getContours(frameDil, frameContour)

    frameMask = frame.copy()
    frameSquares = frame.copy()
    frameMaskImg = frame.copy()

    if points is not None:
        if len(points) == NUM_POINTS:
            # frameMask = drawPoints(points, frameMask)
            frameMask = np.zeros(frame.shape, dtype=np.uint8)
            frameMask = cv.rectangle(frameMask, [points[0][0][0], points[0][0][1]], [points[2][0][0], points[2][0][1]], (255, 255, 255), -1)

            # Mask input image with binary mask
            frameMaskImg = cv.bitwise_and(frame, frameMask)
            # Color background white
            frameMaskImg[frameMask == 0] = 255

            squares = find_squares(frameMaskImg)
            frameSquares = cv.drawContours(frameSquares, squares, -1, (0, 255, 0), 3)

            for square in squares:
                x = square[0][0].item() + 20
                y = square[0][1].item() + 20
                colors = ComputerVisionRubiksRGB.RGBUint8.identifyBGR(frame, x, y)
                cv.circle(frameSquares, (x, y), 2, (0, 0, 0), 2)
                cv.putText(frameSquares, "Color: " + str(colors), (square[0][0], square[0][1]), cv.FONT_HERSHEY_COMPLEX,
                            .7,
                            (0, 255, 0), 2)
            # colorsB = frame[y, x, 0]
            # colorsG = frame[y, x, 1]
            # colorsR = frame[y, x, 2]
            # colors = frame[y, x]
            # print("Red: ", colorsR)
            # print("Green: ", colorsG)
            # print("Blue: ", colorsB)
            # print("BRG Format: ", colors)

    frameStack = stackFrames(0.8, ([frame, frameCanny, frameGray],
                                   [frameDil, frameBlur, frameContour],
                                   [frameMask, frameMaskImg, frameSquares]))

    cv.imshow('Rubiks Cube Viewer', frameStack)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
