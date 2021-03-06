from fbchat import Client
from fbchat.models import *
from detector import Webcam, ImageProcessor
from datetime import timedelta
import logging
import cv2
import config
import time


class Butler(Client):
  def __init__(self, email, password, outputDir):
    Client.__init__(self, email, password)
    self.outputDir = outputDir

  def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
    self.markAsDelivered(thread_id, message_object.uid)
    self.markAsRead(thread_id)
    if message_object.text and (message_object.text.lower() == 'status' or message_object.text == u"\U0001F697"):
      self.serviceStatusMessage(
          author_id, message_object, thread_id, thread_type)

  def serviceStatusMessage(self, author_id, message_object, thread_id, thread_type):
    camera = Webcam(1)
    start_time = time.time()
    while (time.time() - start_time) < 3.0:
      success, img = camera.getSnapshotCV()
    camera.release()
    if not success:
      return
    path_to_img = self.outputDir + '/request_status.png'
    cv2.imwrite(path_to_img, img)
    proc = ImageProcessor(config.THRESHOLD, config. SHAPES,
                          config.TEMPLATEDIR, config.OUTPUTDIR, config.HORIZ_ALIGN_THRESH)
    curr_door_state, _ = proc.detectGarageDoorState(img)
    msg_txt = "Garage door is " + curr_door_state.name + ' at ' + time.asctime()
    try:
      self.sendLocalImage(path_to_img,
                          message=Message(text=msg_txt), thread_id=thread_id, thread_type=thread_type)
    except (FBchatException, e):
      print("FBchatException caught!", e.fb_error_message)

  def closeGarageReminder(self, elapsed):
    msg_txt = "Garage has been opened for " + \
        str(timedelta(seconds=int(elapsed))) + \
        '. Chippie feels cold please close the FUCKING GARAGE.'
    img_to_send = self.createScaryImage()
    self.send(Message(text=msg_txt), thread_id=config.JJ_ID,
              thread_type=ThreadType.USER)
    try:
      msg_id = self.sendLocalImage(
          img_to_send, thread_id=config.JJ_ID, thread_type=ThreadType.USER)
      print("sent message id:", msg_id)
      self.reactToMessage(msg_id, MessageReaction.ANGRY)
    except (FBchatException, e):
      print("FBchatException caught!", e.fb_error_message)

  def createScaryImage(self):
    img1 = cv2.imread(
        "/home/pi/garage_monitor/saved_images/last_image.png")
    img2 = cv2.imread(
        "/home/pi/garage_monitor/saved_images/aggretsuko.png")[:1080]
    img3 = cv2.addWeighted(img1, .75, img2, 0.3, 0)
    overlay_path = "/home/pi/garage_monitor/saved_images/angery_reacc.png"
    cv2.imwrite(overlay_path, img3)
    return overlay_path
