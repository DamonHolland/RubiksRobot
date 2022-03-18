import cv2 as opencv
import cv.ComputerVisionRubiksRGB as CV_Rgb
from model.RubiksCube import RubiksCube


def draw_pixels(frame, pixel_array):
    for row in pixel_array:
        for pixel in row:
            opencv.circle(frame, (pixel[0], pixel[1]), 5, (255, 255, 255), 2)


class ComputerVisionStatic:
    def __init__(self, file_name, top_cam, bottom_cam):
        self.frameWidth = 720
        self.frameHeight = 720

        self.capTop = None
        self.capBot = None
        self.set_top_cam(top_cam)
        if top_cam == bottom_cam: self.capBot = self.capTop
        else: self.set_bottom_cam(bottom_cam)
        self.frame_top = None
        self.frame_bot = None

        # White, Red, Blue
        self.colorsTop = [[(0, 0) for _i in range(9)], [(0, 0) for _i in range(9)], [(0, 0) for _i in range(9)]]
        # Orange, Green, Yellow
        self.colorsBot = [[(0, 0) for _i in range(9)], [(0, 0) for _i in range(9)], [(0, 0) for _i in range(9)]]

        self.load_pixels(file_name)

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

    def save_pixels(self, file_name):
        file = open(file_name, "r+")

        for row in self.colorsTop:
            for pixel in row:
                file.write(str(pixel[0]) + " " + str(pixel[1]) + "\n")

        for row in self.colorsBot:
            for pixel in row:
                file.write(str(pixel[0]) + " " + str(pixel[1]) + "\n")

    def load_pixels(self, file_name):
        file = open(file_name, "r")
        for row in self.colorsTop:
            for i in range(len(row)):
                txt = file.readline().split()
                new_pixel = (int(txt[0]), int(txt[1]))
                row[i] = new_pixel

        for row in self.colorsBot:
            for i in range(len(row)):
                txt = file.readline().split()
                new_pixel = (int(txt[0]), int(txt[1]))
                row[i] = new_pixel

    def scan_cube(self):
        ret_top, self.frame_top = self.capTop.read()
        ret_bot, self.frame_bot = self.capBot.read()
        if not ret_top or not ret_bot: return None
        draw_pixels(self.frame_top, self.colorsTop)
        draw_pixels(self.frame_bot, self.colorsBot)
        encoding = self._generate_encoding()
        # merged = opencv.vconcat([self.frame_top, self.frame_bot])
        # opencv.imshow('Cube Cams', merged)
        return encoding

    def _generate_encoding(self):
        # Convert Cube
        encoding = [CV_Rgb.RGBUint8.identifyOneHot(self.frame_top, p[0], p[1]) for p in self.colorsTop[0]]  # White
        encoding += [CV_Rgb.RGBUint8.identifyOneHot(self.frame_bot, p[0], p[1]) for p in self.colorsBot[1]]  # Green
        encoding += [CV_Rgb.RGBUint8.identifyOneHot(self.frame_top, p[0], p[1]) for p in self.colorsTop[1]]  # Red
        encoding += [CV_Rgb.RGBUint8.identifyOneHot(self.frame_top, p[0], p[1]) for p in self.colorsTop[2]]  # Blue
        encoding += [CV_Rgb.RGBUint8.identifyOneHot(self.frame_bot, p[0], p[1]) for p in self.colorsBot[0]]  # Orange
        encoding += [CV_Rgb.RGBUint8.identifyOneHot(self.frame_bot, p[0], p[1]) for p in self.colorsBot[2]]  # Yellow
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
