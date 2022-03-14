import numpy as np
import cv2 as cv


class RGBUint8:
    def identifyHue(frame, x, y):
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        pixel_center = hsv_frame[y, x]
        hue_value = pixel_center[0]

        return hue_value;

    def identifyRGB(frame, x, y):
        pixel_center_bgr = frame[y, x]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        return (b, g, r);


    def identifyOneHot(frame, x, y):
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        
        pixel_center = hsv_frame[y, x]
        hue_value = pixel_center[0]

        color = None

        if hue_value < 5:
            # Red
            color = (0, 0, 0, 1, 0, 0)
        elif hue_value < 22:
            # Orange
            color = (0, 1, 0, 0, 0, 0)
        elif hue_value < 39:
            # Yellow
            color = (1, 0, 0, 0, 0, 0)
        elif hue_value < 80:
            # Green
            color = (0, 0, 0, 0, 1, 0)
        elif hue_value < 131:
            # Blue
            color = (0, 0, 1, 0, 0, 0)
        else:
            # Red
            color = (0, 0, 0, 1, 0, 0)

        pixel_center_bgr = frame[y, x]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        if b > 160 and g > 160 and r > 160:
            # White
            color = (0, 0, 0, 0, 0, 1)

        return color
