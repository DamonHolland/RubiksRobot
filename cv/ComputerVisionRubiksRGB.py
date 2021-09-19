import numpy as np


class RGBUint8:
    WHITE_MIN = np.array([160, 160, 160], np.uint8)
    WHITE_MAX = np.array([255, 255, 255], np.uint8)

    BLUE_MIN = np.array([10, 10, 50], np.uint8)
    BLUE_MAX = np.array([100, 100, 255], np.uint8)

    RED_MIN = np.array([50, 10, 10], np.uint8)
    RED_MAX = np.array([255, 100, 100], np.uint8)

    YELLOW_MIN = np.array([20, 60, 60], np.uint8)
    YELLOW_MAX = np.array([60, 255, 255], np.uint8)

    GREEN_MIN = np.array([10, 50, 10], np.uint8)
    GREEN_MAX = np.array([100, 255, 100], np.uint8)

    ORANGE_MIN = np.array([15, 30, 50], np.uint8)
    ORANGE_MAX = np.array([255, 165, 255], np.uint8)
