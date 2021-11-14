import numpy as np
import cv2 as cv


class RGBUint8:
    def identifyBGR(frame, x, y):
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        
        pixel_center = hsv_frame[y, x]
        hue_value = pixel_center[0]

        color = "Undefined"

        if hue_value < 5:
            color = "RED"
        elif hue_value < 22:
            color = "ORANGE"
        elif hue_value < 33:
            color = "YELLOW"
        elif hue_value < 78:
            color = "GREEN"
        elif hue_value < 131:
            color = "BLUE"
        elif hue_value < 170:
            color = "VIOLET"
        else:
            color = "RED"

        pixel_center_bgr = frame[y, x]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        if b > 150 and g > 150 and r > 150:
            color = "WHITE"

        if b < 30 and g < 30 and r < 30:
            color = "BLACK"

        return color
