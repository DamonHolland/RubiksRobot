import cv2 as cv
import numpy as np
import ComputerVisionRubiksRGB

frameWidth = 720
frameHeight = 720
cap = cv.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

colors = [[(128, 158), (), (), (), (), (), (), ()],
          [(), (), (), (), (), (), (), ()],
          [(), (), (), (), (), (), (), ()]]

test = [[(135, 161)],
        [(158, 154)],
        [(195, 141)]]

if not cap.isOpened():
    print("Camera cannot be opened. Exiting...")
    exit()


def drawCircle (frame, pixelArray):
    for row in pixelArray:
        for pixel in row:
            cv.circle(frame, (pixel[0], pixel[1]), 5, (255, 255, 255), 2)

    return frame


def defineColors (frame, pixelArray):
    for row in pixelArray:
        for pixel in row:
            print("Coordinates: (", str(pixel[0]), ", ", str(pixel[1]), ") is ", ComputerVisionRubiksRGB.RGBUint8.identifyBGR(frame, pixel[0], pixel[1]))


if __name__ == '__main__':
    while True:
        ret, frame = cap.read()

        frame = drawCircle(frame, test)

        cv.imshow('Rubiks Cube Viewer', frame)

        if cv.waitKey(1) == ord('q'):
            defineColors(frame, test)
            break

    cap.release()
    cv.destroyAllWindows()