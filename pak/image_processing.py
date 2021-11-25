import time
import cv2
import pytesseract
from pak.time import stopwatch
import numpy as np
from cv2 import COLOR_BGR2GRAY
from PIL import Image


class ImageProcessing(object):
    @staticmethod
    def open_image2np(file_dir: str):
        return np.array(Image.open(file_dir))

    def grayscale_image(self, data_array):
        return cv2.cvtColor(data_array, cv2.COLOR_BGR2GRAY)

    def resize_image(self, data_array, width, height):
        return cv2.resize(data_array, (width, height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

    def crop_image(self, data_array, width_from=None, width_to=None, height_from=None, height_to=None):
        """
        Image pixel arrangement as follows (example of 1920 x 1080):
                       Width
                  0   ---------- 1919
                  |               |
          Height  |               |
                  |               |
                 1079 ----------
        """
        return data_array[height_from:height_to, width_from:width_to]

    def get_image_text(self, data_array, psm=3, oem=None):
        if oem is not None:
            oem_conf = f'--oem {oem}'
        else:
            oem_conf = None
        return pytesseract.image_to_string(data_array, config=f'--psm {psm}{oem_conf}')

    @staticmethod
    def show_image(image_data):
        import matplotlib.pyplot as plt
        if image_data.ndim == 2:  # grayscale image
            plt.imshow(image_data, cmap='gray', vmin=0, vmax=255)
        elif image_data.ndim == 3:  # colour image
            plt.imshow(image_data)
        plt.show()


class VideoProcessing(ImageProcessing):
    def __init__(self, video_path):
        super().__init__()
        self.cap = cv2.VideoCapture(video_path)
        self.__reset()
        self.preload()

    def __reset(self):
        self.width = int
        self.height = int
        self.frames_total = 0
        self.frames = []

    @property
    def resolution(self):
        return self.width, self.height

    @stopwatch
    def preload(self):
        self.__reset()
        while self.cap.isOpened():
            flag, frame = self.cap.read()
            if not flag:
                break
            self.frames_total += 1
            self.frames.append(frame)
        self.height = len(self.frames[0])  # Assume all frames in video are same w x h
        self.width = len(self.frames[0][0])
        return self.frames

    def get_frame(self, index: int):
        if index > self.frames_total:
            raise IndexError('index shall be less than total frame count')
        return self.frames[index]
