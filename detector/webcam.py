import cv2


class Webcam:
  def __init__(self, capture):
    self.cap = cv2.VideoCapture(capture)
    self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

  def getSnapshotCV(self):
    for i in range(100):
      success, frame = self.cap.read()
      return success, frame

  def release(self):
    self.cap.release()


def test():
  cam = Webcam(1)
  success, img = cam.getSnapshotCV()
  cv2.imwrite("/home/pi/garage_monitor/saved_images/test.png", img)


# test()
