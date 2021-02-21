import cv2


class VideoCamera:
    def __init__(self):
        self.camera = cv2.VideoCapture()
        self.camera.set(3, 1920 * 0.3)
        self.camera.set(4, 1080 * 0.3)

    def get_frame(self):
        _, frame = self.camera.read()
        frame = cv2.flip(frame, 1)
        success, frame = cv2.imencode(".jpg", frame)
        return frame

    @property
    def is_opened(self):
        return self.camera.isOpened()

    def open(self):
        if not self.camera.isOpened():
            self.camera.open(0)

    def close(self):
        if self.camera.isOpened():
            self.camera.release()
