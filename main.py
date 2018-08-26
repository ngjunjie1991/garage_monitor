import config
import sys
import traceback
import time
import cv2

from detector import Webcam, ImageProcessor, GarageDoorDetectionState

if __name__ == '__main__':
  prev_door_state = GarageDoorDetectionState.CLOSED
  try:
    camera = Webcam(0)
    while True:
      img = camera.getSnapshotCV()
      proc = ImageProcessor(config.THRESHOLD, config. SHAPES,
                            config.TEMPLATEDIR, config.OUTPUTDIR, config.HORIZ_ALIGN_THRESH)
      curr_door_state, detected_shapes = proc.detectGarageDoorState(img)
      if curr_door_state == GarageDoorDetectionState.OPEN and prev_door_state == GarageDoorDetectionState.OPEN:
        print("****ALARM ALARM YOU FORGOT TO CLOSE THE FUCKING DOOR AGAIN*****")
      print("Door is", curr_door_state.name)
      prev_door_state = curr_door_state
      time.sleep(5 * 60)
  except Exception as e:
    print('Fatal error')
    print(e)
    print(traceback.format_exc())
    camera.release()
    sys.exit()
