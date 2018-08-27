import config
import sys
import traceback
import time
import cv2

from detector import Webcam, ImageProcessor, GarageDoorDetectionState
from chatbot import Butler

if __name__ == '__main__':
  door_open_time = time.time()
  prev_door_state = GarageDoorDetectionState.CLOSED
  try:
    alfred = Butler(config.BOT_EMAIL, config.BOT_PASSWORD, config.OUTPUTDIR)
    while True:
      camera = Webcam(0)
      success, img = camera.getSnapshotCV()
      if not success:
        continue
      proc = ImageProcessor(config.THRESHOLD, config. SHAPES,
                            config.TEMPLATEDIR, config.OUTPUTDIR, config.HORIZ_ALIGN_THRESH)
      curr_door_state, detected_shapes = proc.detectGarageDoorState(img)

      if curr_door_state == GarageDoorDetectionState.OPEN and prev_door_state == GarageDoorDetectionState.OPEN:
        alfred.closeGarageReminder(time.time() - door_open_time)
      else:
        door_open_time = time.time()

      print("Door is", curr_door_state.name)
      prev_door_state = curr_door_state
      camera.release()
      time.sleep(4.5 * 60)
  except Exception as e:
    print('Fatal error')
    print(e)
    print(traceback.format_exc())
    camera.release()
    sys.exit()
