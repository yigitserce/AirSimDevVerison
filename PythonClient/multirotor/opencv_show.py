# In settings.json first activate computer vision mode:
# https://github.com/Microsoft/AirSim/blob/main/docs/image_apis.md#computer-vision-mode

import setup_path
import airsim

# requires Python 3.5.3 :: Anaconda 4.4.0
# pip install opencv-python
import cv2
import time
import sys

cameraType = "scene"

for arg in sys.argv[1:]:
  cameraType = arg.lower()

cameraTypeMap = {
 "depth": airsim.ImageType.DepthVis,
 "segmentation": airsim.ImageType.Segmentation,
 "seg": airsim.ImageType.Segmentation,
 "scene": airsim.ImageType.Scene,
 "disparity": airsim.ImageType.DisparityNormalized,
 "normals": airsim.ImageType.SurfaceNormals
}

client = airsim.MultirotorClient()

print("Connected: ")

fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
thickness = 2
textSize, baseline = cv2.getTextSize("FPS", fontFace, fontScale, thickness)
print(textSize)
textOrg = (10, 10 + textSize[1])
frameCount = 0
startTime = time.time()
fps = 0

# 1280x720, 30fps, h265
camera = cv2.VideoCapture(0)

gstreamer_pipeline = 'width=640, height=480 ! mpegtsmux ! udpsink host=127.0.0.1 port=5000 sync=false'
# gstreamer_pipeline = 'appsrc ! videoconvert ! videoscale ! video/x-raw, width=640, height=480 ! x264enc ! mpegtsmux !udpsink host=127.0.0.1 port=5000 sync=false'
out = cv2.VideoWriter(gstreamer_pipeline, cv2.CAP_GSTREAMER, 0, 5, (640, 480), True)

if not out.isOpened():
  print("Could not open VideoWriter")
  sys.exit(0)


while True:
  # rawImage = client.simGetImage("0", cameraTypeMap[cameraType])
  # if (rawImage == None):
  #     print("Camera is not returning image, please check airsim for error messages")
  #     sys.exit(0)
  # else:
  #     png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
  #     cv2.putText(png,'FPS ' + str(fps),textOrg, fontFace, fontScale,(255,0,255),thickness)
  #     cv2.imshow("Camera 0", png)
  
  check, frame = camera.read()
  frame = cv2.resize(frame, (640, 480))
  out.write(frame)
  out.release()
  # frameCount = frameCount  + 1
  # endTime = time.time()
  # diff = endTime - startTime
  # if (diff > 1):
  #     fps = frameCount
  #     frameCount = 0
  #     startTime = endTime

  # key = cv2.waitKey(1) & 0xFF
  # if (key == 27 or key == ord('q') or key == ord('x')):
  #     break
