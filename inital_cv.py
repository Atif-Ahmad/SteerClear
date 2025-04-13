import numpy as np
import cv2
from scipy.spatial import distance as dist



cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)[0:1]
        if len(eyes) == 0:
            print("User's eyes are closed")
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
            eye = roi_gray[ey:ey + eh, ex:ex + ew]

            _, binary = cv2.threshold(eye, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Calculate total pixels in the eye region
            total_pixels = binary.size

            # Count white pixels (value == 255)
            white_pixels = cv2.countNonZero(binary)

            # Calculate openness ratio (0 = fully closed, 1 = fully open)
            openness_ratio = white_pixels / total_pixels

            print(f"Eye openness: {openness_ratio:.2f}")
            cv2.imshow('Thresholded Eye', binary)

            if (openness_ratio < 0.4):
                print("User displaying signs of drowsiness")
            

    # cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
