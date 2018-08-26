import numpy as np
import cv2
from detector.shape import Shape
import time
from enum import Enum


class GarageDoorDetectionState(Enum):
  FAILED = 1
  OPEN = 2
  CLOSED = 3


class ImageProcessor:
  def __init__(self, threshold, shapes, templateDir, outputDir, horizAlignThreshold):
    self.detectionThreshold = threshold
    self.shapesToDetect = shapes
    self.templateDir = templateDir
    self.outputDir = outputDir
    self.horizAlignThreshold = horizAlignThreshold

  def detectAndOverlay(self, img, shape):
    img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_equalized = cv2.equalizeHist(img_grayscale)
    cv2.imwrite(self.outputDir + '/last_image.png', img_equalized)
    result = cv2.matchTemplate(
        img_equalized, shape.templateImage, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(shape.name, min_val, max_val)

    if max_val >= (self.detectionThreshold / 100):
      top_left = max_loc
      bottom_right = (top_left[0] + shape.width, top_left[1] + shape.height)
      shape.setMatchInfo(top_left, bottom_right, max_val)

    return

  def findShapes(self, img):
    shapes_dict = {}
    for shape_name in self.shapesToDetect:
      shape_to_detect = Shape(
          shape_name, self.templateDir + '/' + shape_name + '_template.png')
      self.detectAndOverlay(img, shape_to_detect)
      shapes_dict[shape_name] = shape_to_detect
    return shapes_dict

  def detectGarageDoorState(self, img):
    detected_shapes = self.findShapes(img)
    state = GarageDoorDetectionState.FAILED
    detected_shapes_count = 0
    for _, shape in detected_shapes.items():
      if shape.detected == True:
        detected_shapes_count += 1

    if detected_shapes_count == len(detected_shapes):
      # cv2.rectangle(img, detected_shapes['triangle'].topLeft,
      #               detected_shapes['triangle'].bottomRight, (0, 255, 0), 2)
      # cv2.rectangle(img, detected_shapes['pentagon'].topLeft,
      #               detected_shapes['pentagon'].bottomRight, (0, 255, 0), 2)
      # cv2.imshow("Door closed", img)
      # cv2.waitKey(0)
      triangle_left = detected_shapes['triangle'].topLeft[0]
      pentagon_left = detected_shapes['pentagon'].topLeft[0]
      x_diff = abs(triangle_left - pentagon_left)
      if x_diff <= self.horizAlignThreshold:
        state = GarageDoorDetectionState.CLOSED
      else:
        state = GarageDoorDetectionState.FAILED

    else:
      # cv2.imshow("Door open", img)
      # cv2.waitKey(0)
      state = GarageDoorDetectionState.OPEN

    return state, detected_shapes
