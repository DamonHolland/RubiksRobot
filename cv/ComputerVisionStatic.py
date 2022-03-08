import cv2 as opencv
import cv.ComputerVisionRubiksRGB as ComputerVisionRubiksRGB
from model.RubiksCube import RubiksCube


class ComputerVisionStatic:
    def __init__(self):
        self.frameWidth = 720
        self.frameHeight = 720
        self.capTop = opencv.VideoCapture(0)
        self.capBot = opencv.VideoCapture(1)

        self.capTop.set(3, self.frameWidth)
        self.capTop.set(4, self.frameHeight)

        self.capBot.set(3, self.frameWidth)
        self.capBot.set(4, self.frameHeight)

        self.colorsTop = [
            [(327, 108), (353, 120), (383, 142), (272, 122), (305, 134), (356, 163), (245, 141), (272, 165), (318, 187)],
            [(232, 180), (268, 196), (299, 217), (224, 208), (255, 228), (301, 250), (223, 241), (270, 284), (305, 297)],
            [(335, 231), (378, 197), (398, 181), (337, 254), (369, 233), (408, 203), (342, 297), (361, 282), (407, 236)]]

        self.colorsBot = [
            [(403, 265), (352, 301), (330, 315), (408, 234), (362, 262), (331, 275), (408, 209), (367, 226), (328, 245)],
            [(296, 312), (270, 297), (229, 259), (295, 278), (261, 248), (228, 221), (298, 245), (260, 214), (232, 192)],
            [(314, 207), (279, 184), (248, 159), (358, 191), (320, 159), (280, 137), (389, 170), (366, 148), (338, 127)]]

        self.onehotencoding = []

    def drawCircle(self, frame, pixelArray):
        for row in pixelArray:
            for pixel in row:
                opencv.circle(frame, (pixel[0], pixel[1]), 5, (255, 255, 255), 2)

        return frame

    def defineColors(self, frame, pixelArray, retVal):
        for row in pixelArray:
            for pixel in row:
                retVal.append(ComputerVisionRubiksRGB.RGBUint8.identifyBGR(frame, pixel[0], pixel[1]))

        return retVal

    def scanCube(self):
        while True:
            retTop, frameTop = self.capTop.read()
            retBot, frameBot = self.capBot.read()

            frameTop = self.drawCircle(frameTop, self.colorsTop)
            frameBot = self.drawCircle(frameBot, self.colorsBot)

            opencv.imshow('Rubiks Cube Top', frameTop)
            opencv.imshow('Rubiks Cube Bot', frameBot)

            self.defineColors(frameTop, self.colorsTop, self.onehotencoding)
            self.defineColors(frameBot, self.colorsBot, self.onehotencoding)

            if (opencv.waitKey(1) == ord('q')):
                self.onehotencoding[4] = RubiksCube.WHITE
                self.onehotencoding[13] = RubiksCube.RED
                self.onehotencoding[22] = RubiksCube.BLUE
                self.onehotencoding[31] = RubiksCube.ORANGE
                self.onehotencoding[40] = RubiksCube.GREEN
                self.onehotencoding[49] = RubiksCube.YELLOW

                self.capTop.release()
                self.capBot.release()
                opencv.destroyAllWindows()

                return self.onehotencoding
