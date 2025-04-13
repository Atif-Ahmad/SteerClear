import time
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

i = 0
while True:
    time.sleep(2)
    picam2.capture_file(f"test_{i}.jpg")
    i = i + 1
