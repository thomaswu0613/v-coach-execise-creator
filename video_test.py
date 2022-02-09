#/home/thomasw/workspace/v-coach-execise-creator/IMG_105610890.MOV

from unittest.mock import NonCallableMagicMock
from vidgear.gears import VideoGear
import numpy as np
import cv2

# open any valid video stream with stabilization enabled(`stabilize = True`)
stream_stab = VideoGear(source="/home/thomasw/workspace/v-coach-execise-creator/IMG_105610890.MOV",framerate=15).start()

while True:
    frame_stab = stream_stab.read()
    if frame_stab is None:
        break
    cv2.imshow("test", frame_stab)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
stream_stab.stop()