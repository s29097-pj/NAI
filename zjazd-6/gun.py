# Autorzy: Aleksander Bastek, Michał Małolepszy
# Opis działania: Program wykrywa ruszającą się twarz. Na jej czole rysuje celownik, podczas ruchu.
# Sposób użycia: python gun.py

import cv2

face_cascade = cv2.CascadeClassifier(
        'haar_cascade_files/haarcascade_frontalface_default.xml')

if face_cascade.empty():
	raise IOError('Unable to load the face cascade classifier xml file')

bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=5, detectShadows=True)
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    fg_mask = bg_subtractor.apply(frame)

    _, fg_mask = cv2.threshold(fg_mask, 150, 255, cv2.THRESH_BINARY)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in face_rects:
        face_roi_mask = fg_mask[y:y + h, x:x + w]
        motion_pixels = cv2.countNonZero(face_roi_mask)
        if motion_pixels > (w * h * 0.05):
            cv2.circle(frame, ((x+w//2), y+h//10), 30, (0,0,255), 2)
            cv2.line(frame, ((x+w//2-30), y+h//10), ((x+w//2+30), y+h//10), (0,0,255), 1)
            cv2.line(frame, ((x+w//2), y+h//10+30), ((x+w//2), y+h//10-30), (0,0,255), 1)

    cv2.imshow('Face Detector', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
