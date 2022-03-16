import cv2 as opencv
import cv.ComputerVisionRubiksRGB as ComputerVisionRubiksRGB
from model.RubiksCube import RubiksCube


class ComputerVisionStatic:
    def __init__(self):
        self.fileName = "saved_pixels.txt"

        self.frameWidth = 720
        self.frameHeight = 720

        self.camTop = 0
        self.camBot = 1

        self.capTop = None
        self.capBot = None

        self.retBot = None
        self.frameBot = None

        self.retTop = None
        self.frameTop = None

        self.colorsTop = [
            [(385, 144), (347, 162), (314, 181), (351, 121), (316, 141), (277, 157), (323, 107), (277, 119),
             (240, 136)],  # White
            [(222, 167), (262, 192), (293, 212), (221, 204), (254, 230), (289, 251), (220, 236), (253, 268),
             (289, 291)],  # Red
            [(329, 217), (370, 192), (403, 176), (330, 257), (364, 238), (398, 213), (326, 295), (359, 274), (386, 259)]
            # Blue
        ]

        self.colorsBot = [
            [(395, 283), (359, 313), (325, 330), (401, 252), (365, 278), (324, 299), (400, 221), (367, 239),
             (330, 263)],  # Orange
            [(288, 333), (259, 309), (238, 292), (293, 295), (255, 271), (227, 251), (291, 259), (258, 239),
             (225, 217)],  # Green
            [(383, 184), (347, 205), (306, 228), (350, 161), (312, 184), (276, 205), (325, 145), (279, 160), (241, 188)]
            # Yellow
        ]

        self.onehotencoding = []

    def initCameras(self):
        self.capTop = opencv.VideoCapture(self.camTop)
        self.capBot = opencv.VideoCapture(self.camBot)

        self.capTop.set(3, self.frameWidth)
        self.capTop.set(4, self.frameHeight)

        self.capBot.set(3, self.frameWidth)
        self.capBot.set(4, self.frameHeight)

    def switchCameras(self):
        temp = self.camBot
        self.camBot = self.camTop
        self.camTop = temp;
        self.initCameras()

    def switchCamTop(self, num):
        self.camTop = num
        self.initCameras()

    def switchCamBot(self, num):
        self.camBot = num
        self.initCameras()

    def drawCircle(self, frame, pixelArray):
        for row in pixelArray:
            for pixel in row:
                opencv.circle(frame, (pixel[0], pixel[1]), 5, (255, 255, 255), 2)

        return frame

    def savePixels(self):
        writeFile = open(self.fileName, "r+")

        for row in self.colorsTop:
            for pixel in row:
                writeFile.write(str(pixel[0]) + " " + str(pixel[1]) + "\n")

        for row in self.colorsBot:
            for pixel in row:
                writeFile.write(str(pixel[0]) + " " + str(pixel[1]) + "\n")

    def loadPixels(self):
        readFile = open(self.fileName, "r")

        for row in self.colorsTop:
            for pixel in row:
                txt = readFile.readline().split()
                newPixel = (int(txt[0]), int(txt[1]))
                pixel = newPixel

                print(pixel)

        for row in self.colorsBot:
            for pixel in row:
                txt = readFile.readline().split()
                newPixel = (int(txt[0]), int(txt[1]))
                pixel = newPixel

                print(pixel)


    def scanCube(self):
        while True:
            self.retTop, self.frameTop = self.capTop.read()
            self.retBot, self.frameBot = self.capBot.read()

            self.frameTop = self.drawCircle(self.frameTop, self.colorsTop)
            self.frameBot = self.drawCircle(self.frameBot, self.colorsBot)

            opencv.imshow('Rubiks Cube Top', self.frameTop)
            opencv.imshow('Rubiks Cube Bot', self.frameBot)

    def produceOneHot(self):
        for pixel in self.colorsTop[0]:  # White
            self.onehotencoding.append(
                ComputerVisionRubiksRGB.RGBUint8.identifyOneHot(self.frameTop, pixel[0], pixel[1]))

        for pixel in self.colorsBot[1]:  # Green
            self.onehotencoding.append(
                ComputerVisionRubiksRGB.RGBUint8.identifyOneHot(self.frameBot, pixel[0], pixel[1]))

        for pixel in self.colorsTop[1]:  # Red
            self.onehotencoding.append(
                ComputerVisionRubiksRGB.RGBUint8.identifyOneHot(self.frameTop, pixel[0], pixel[1]))

        for pixel in self.colorsTop[2]:  # Blue
            self.onehotencoding.append(
                ComputerVisionRubiksRGB.RGBUint8.identifyOneHot(self.frameTop, pixel[0], pixel[1]))

        for pixel in self.colorsBot[0]:  # Orange
            self.onehotencoding.append(
                ComputerVisionRubiksRGB.RGBUint8.identifyOneHot(self.frameBot, pixel[0], pixel[1]))

        for pixel in self.colorsBot[2]:  # Yellow
            self.onehotencoding.append(
                ComputerVisionRubiksRGB.RGBUint8.identifyOneHot(self.frameBot, pixel[0], pixel[1]))

        self.onehotencoding[4] = RubiksCube.WHITE
        self.onehotencoding[13] = RubiksCube.GREEN
        self.onehotencoding[22] = RubiksCube.RED
        self.onehotencoding[31] = RubiksCube.BLUE
        self.onehotencoding[40] = RubiksCube.ORANGE
        self.onehotencoding[49] = RubiksCube.YELLOW

        return self.onehotencoding

    def terminateCameras(self):
        self.capTop.release()
        self.capBot.release()
        opencv.destroyAllWindows()
