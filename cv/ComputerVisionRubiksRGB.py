import numpy as np
import cv2 as cv


class RGBUint8:
    def identifyBGR(frame, x, y):
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        
        pixel_center = hsv_frame[y, x]
        hue_value = pixel_center[0]

        color = "Undefined"

        if hue_value < 5:
            #RED
            color = (0, 0, 0, 1, 0, 0)
        elif hue_value < 22:
            #ORANGE
            color = (0, 1, 0, 0, 0, 0)
        elif hue_value < 33:
            #YELLOW
            color = (1, 0, 0, 0, 0, 0)
        elif hue_value < 78:
            #GREEN
            color = (0, 0, 0, 0, 1, 0)
        elif hue_value < 131:
            #BLUE
            color = (0, 0, 1, 0, 0, 0)
        else:
            #RED
            color = (0, 0, 0, 1, 0, 0)

        pixel_center_bgr = frame[y, x]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        if b > 150 and g > 150 and r > 150:
            color = (0, 0, 0, 0, 0, 1)

        return color
