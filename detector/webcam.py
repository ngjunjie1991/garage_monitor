import cv2
import time


class Webcam:
  def __init__(self, capture):
    while True:
      self.cap = cv2.VideoCapture(capture)
      if self.cap.isOpened():
        break
      time.sleep(3)

    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

  def getSnapshotCV(self):
    return self.cap.read()

  def release(self):
    self.cap.release()
