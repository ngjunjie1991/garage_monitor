from fbchat import Client
from fbchat.models import *
from detector import Webcam, ImageProcessor
import logging
import cv2
import config


class Butler(Client):
  def __init__(self, email, password, outputDir):
    Client.__init__(self, email, password)
    self.outputDir = outputDir

  def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
    self.markAsDelivered(thread_id, message_object.uid)
    self.markAsRead(thread_id)

    # If you're not the author, echo
    if message_object.text.lower() == 'status':
      self.serviceStatusMessage(
          author_id, message_object, thread_id, thread_type)

  def serviceStatusMessage(self, author_id, message_object, thread_id, thread_type):
    camera = Webcam(1)
    success = False
    success, img = camera.getSnapshotCV()
    camera.release()
    if not success:
      return
    path_to_img = self.outputDir + '/request_status.png'
    cv2.imwrite(path_to_img, img)
    proc = ImageProcessor(config.THRESHOLD, config. SHAPES,
                          config.TEMPLATEDIR, config.OUTPUTDIR, config.HORIZ_ALIGN_THRESH)
    curr_door_state, _ = proc.detectGarageDoorState(img)
    msg_txt = "Garage door is " + curr_door_state.name
    self.sendLocalImage(path_to_img,
                        message=Message(text=msg_txt), thread_id=thread_id, thread_type=thread_type)

  def closeGarageReminder(self, thread_id, thread_type):
    last_saved_image = '/home/pi/garage_monitor/saved_images/last_image.png'
    self.sendLocalImage(last_saved_image, message=Message(
        text='Somebody gonna get a hurt real bad'), thread_id=thread_id, thread_type=thread_type)
