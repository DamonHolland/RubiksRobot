import cv2 as opencv
import cv.ComputerVisionRubiksRGB as CV_Rgb
from model.RubiksCube import RubiksCube


class ComputerVisionStatic:
    def __init__(self, top_cam, bottom_cam):
        self.fileName = "saved_pixels.txt"

        self.frameWidth = 720
        self.frameHeight = 720

        self.capTop = None
        self.set_top_cam(top_cam)
        self.capBot = None
        self.set_bottom_cam(bottom_cam)

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

    def set_top_cam(self, num):
        if self.capTop: self.capTop.release()
        self.capTop = opencv.VideoCapture(num)
        self.capTop.set(3, self.frameWidth)
        self.capTop.set(4, self.frameHeight)

    def set_bottom_cam(self, num):
        if self.capBot: self.capBot.release()
        self.capBot = opencv.VideoCapture(num)
        self.capBot.set(3, self.frameWidth)
        self.capBot.set(4, self.frameHeight)

    def draw_pixels(self, frame, pixel_array):
        for row in pixel_array:
            for pixel in row:
                opencv.circle(frame, (pixel[0], pixel[1]), 5, (255, 255, 255), 2)

    def save_pixels(self):
        file = open(self.fileName, "r+")

        for row in self.colorsTop:
            for pixel in row:
                file.write(str(pixel[0]) + " " + str(pixel[1]) + "\n")

        for row in self.colorsBot:
            for pixel in row:
                file.write(str(pixel[0]) + " " + str(pixel[1]) + "\n")

    def load_pixels(self):
        file = open(self.fileName, "r")

        for row in self.colorsTop:
            for _pixel in row:
                txt = file.readline().split()
                new_pixel = (int(txt[0]), int(txt[1]))
                pixel = new_pixel

                print(pixel)

        for row in self.colorsBot:
            for _pixel in row:
                txt = file.readline().split()
                new_pixel = (int(txt[0]), int(txt[1]))
                pixel = new_pixel

                print(pixel)

    def scan_cube(self):
        ret_top, frame_top = self.capTop.read()
        ret_bot, frame_bot = self.capBot.read()
        if not ret_top or not ret_bot: return None
        self.draw_pixels(frame_top, self.colorsTop)
        self.draw_pixels(frame_bot, self.colorsBot)
        opencv.imshow('Rubiks Cube Top', frame_top)
        opencv.imshow('Rubiks Cube Bot', frame_bot)
        return self._generate_encoding(frame_top, frame_bot)

    def _generate_encoding(self, frame_top, frame_bot):
        # Convert Cube
        encoding = [CV_Rgb.RGBUint8.identifyOneHot(frame_top, p[0], p[1]) for p in self.colorsTop[0]]  # White
        encoding += [CV_Rgb.RGBUint8.identifyOneHot(frame_bot, p[0], p[1]) for p in self.colorsBot[1]]  # Green
        encoding += [CV_Rgb.RGBUint8.identifyOneHot(frame_top, p[0], p[1]) for p in self.colorsTop[1]]  # Red
        encoding += [CV_Rgb.RGBUint8.identifyOneHot(frame_top, p[0], p[1]) for p in self.colorsTop[2]]  # Blue
        encoding += [CV_Rgb.RGBUint8.identifyOneHot(frame_bot, p[0], p[1]) for p in self.colorsBot[0]]  # Orange
        encoding += [CV_Rgb.RGBUint8.identifyOneHot(frame_bot, p[0], p[1]) for p in self.colorsBot[2]]  # Yellow
        # Center Caps
        encoding[4] = RubiksCube.WHITE
        encoding[13] = RubiksCube.GREEN
        encoding[22] = RubiksCube.RED
        encoding[31] = RubiksCube.BLUE
        encoding[40] = RubiksCube.ORANGE
        encoding[49] = RubiksCube.YELLOW
        return encoding

    def terminate_cameras(self):
        if self.capTop: self.capTop.release()
        if self.capBot: self.capBot.release()
        opencv.destroyAllWindows()
