import cv2 as cv
import numpy as np
import ComputerVisionRubiksRGB

class ComputerVisionStatic:

    frameWidth = 720
    frameHeight = 720
    capTop = cv.VideoCapture(2)
    capBot = cv.VideoCapture(1)

    capTop.set(3, frameWidth)
    capTop.set(4, frameHeight)

    capBot.set(3, frameWidth)
    capBot.set(4, frameHeight)

    colorsTop = [[(327, 108), (353, 120), (383, 142), (272, 122), (305, 134), (356, 163), (245, 141), (272, 165), (318, 187)],
              [(232, 180), (268, 196), (299, 217), (224, 208), (255, 228), (301, 250), (223, 241), (270, 284), (305, 297)],
              [(335, 231), (378, 197), (398, 181), (337, 254), (369, 233), (408, 203), (342, 297), (361, 282), (407, 236)]]

    colorsBot = [[(403, 265), (352, 301), (330, 315), (408, 234), (362, 262), (331, 275), (408, 209), (367, 226), (328, 245)],
              [(296, 312), (270, 297), (229, 259), (295, 278), (261, 248), (228, 221), (298, 245), (260, 214), (232, 192)],
              [(314, 207), (279, 184), (248, 159), (358, 191), (320, 159), (280, 137), (389, 170), (366, 148), (338, 127)]]

    onehotencoding = []


    def drawCircle(self, frame, pixelArray):
        for row in pixelArray:
            for pixel in row:
                cv.circle(frame, (pixel[0], pixel[1]), 5, (255, 255, 255), 2)

        return frame


    def defineColors(self, frame, pixelArray, retVal):
        for row in pixelArray:
            for pixel in row:
                retVal.append(ComputerVisionRubiksRGB.RGBUint8.identifyBGR(frame, pixel[0], pixel[1]))

        return retVal

    def scanCube(self):
        while True:
            retTop, frameTop = capTop.read()
            retBot, frameBot = capBot.read()

            frameTop = drawCircle(frameTop, colorsTop)
            frameBot = drawCircle(frameBot, colorsBot)

            cv.imshow('Rubiks Cube Top', frameTop)
            cv.imshow('Rubiks Cube Bot', frameBot)

            if cv.waitKey(1) == ord('q'):
                defineColors(frameTop, colorsTop, onehotencoding)
                defineColors(frameBot, colorsBot, onehotencoding)

                capTop.release()
                capBot.release()
                cv.destroyAllWindows()

                return onehotencoding