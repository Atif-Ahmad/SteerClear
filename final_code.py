import cv2
from time import sleep
from picamera2 import Picamera2
import requests
import base64
import RPi.GPIO as GPIO


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def detect_features_from_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y + w, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)

        if len(eyes) == 0:
            return (frame, True) #Person is detected in the frame and their eyes are closed -> Distracted

        else:
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
            return (frame, False) #Person is detected in the frame and their eyes are open -> Not Distracted

    return (frame, False) #Person not detected in the frame so assume they are not driving


buzzer = 23 #speaker code
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)

picam2 = Picamera2() #initializing camera 
camera_config = picam2.create_still_configuration(main={"size": (1024, 768)}, lores={"size": (640, 480)}, display="lores")
picam2.start()
sleep(2)

while True:
    img = picam2.capture_array()
    print(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    res, closed = detect_features_from_frame(img)
    if closed: #running in while so as long as eyes are closed
        print("User is sleepy")
        #do all the buzzer code here
        GPIO.output(buzzer,GPIO.HIGH)
        print ("Beep")
        sleep(0.5) # Delay in seconds
        GPIO.output(buzzer,GPIO.LOW)
        print ("No Beep")
        sleep(0.5)
        
    cv2.imshow("result", res)

picam2.stop()
picam2.close()


