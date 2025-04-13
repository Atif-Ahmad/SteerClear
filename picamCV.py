import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.start()
time.sleep(2)

while True:
    img = picam2.capture_array()
    print(img)
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        breakv

picam2.stop()
picam2.close()
