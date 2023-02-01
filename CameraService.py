import cv2
import os
from threading import Timer


class CameraService:
    def __init__(self, index, fps=60, width=640, height=480, save_path='recode'):
        self.frame = None
        self.timer = None
        self.writer = None
        self.write_lock = False
        self.fps = fps
        self.cap = cv2.VideoCapture(index)
        self.width = width
        self.height = height
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.save_path = save_path

    def _update(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame = frame
            if self.writer is not None and self.writer.isOpened():
                self.write_lock = True
                self.writer.write(frame)
                self.write_lock = False

        self.timer = Timer(1/self.fps, self._update)
        self.timer.start()

    def start(self):
        self.timer = Timer(0.03, self._update)
        self.timer.start()

    def cancel(self):
        self.frame = None
        self.timer.cancel()

    def read(self):
        return self.frame

    def recode(self, name):
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        self.writer = cv2.VideoWriter(
           f'{self.save_path}/{name}', cv2.CAP_FFMPEG, fourcc=fourcc, fps=self.fps, frameSize=(self.width, self.height))

    def save(self):
        if self.writer is not None and self.writer.isOpened():
            while self.write_lock:
                pass
            self.writer.release()
        self.writer = None
