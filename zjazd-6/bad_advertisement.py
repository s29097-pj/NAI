# Autorzy: Aleksander Bastek, Michał Małolepszy
# Opis działania: Wykrywa kiedy oglądający reklame nie patrzy i wstrzymuje ją do momentu, gdy patrzy.
# Sposób użycia: python bad_advertisement.py

import cv2

eye_cascade = cv2.CascadeClassifier(
        'haar_cascade_files/haarcascade_eye.xml')

if eye_cascade.empty():
	raise IOError('Unable to load the eye cascade classifier xml file')

cap = cv2.VideoCapture(0)
commercial_cap = cv2.VideoCapture('commercial.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eye_circle = eye_cascade.detectMultiScale(gray, 1.3, 5)

    if len(eye_circle) > 0:
        ret_comm, comm_frame = commercial_cap.read()
        
        if not ret_comm:
            commercial_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret_comm, comm_frame = commercial_cap.read()

        if ret_comm:
            cv2.imshow('Commercial', comm_frame)
    else:
        if cv2.getWindowProperty('Commercial', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow('Commercial')

    for (x,y,w,h) in eye_circle:
        cv2.circle(frame, ((x+w//2), y+h//10), 30, (0,0,255), 2)

    cv2.imshow('Eye Detector', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
commercial_cap.release()
cv2.destroyAllWindows()
