# Autorzy: Aleksander Bastek, Michał Małolepszy
# Opis działania: Wykrywa flagę rosji, ukrainy lub polski na podstawie wideo z kamery.
# Sposób użycia: python flag_recognision.py

import cv2
import numpy as np

WHITE  = ((0, 0, 180), (180, 40, 255))
RED1   = ((0, 120, 70), (10, 255, 255))
RED2   = ((170, 120, 70), (180, 255, 255))
BLUE   = ((90, 100, 50), (140, 255, 255))
YELLOW = ((20, 100, 100), (35, 255, 255))


def color_ratio(hsv, lower, upper):
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    return cv2.countNonZero(mask) / (hsv.shape[0] * hsv.shape[1])


def dominant_colors(hsv):
    red = color_ratio(hsv, *RED1) + color_ratio(hsv, *RED2)
    white = color_ratio(hsv, *WHITE)
    blue = color_ratio(hsv, *BLUE)
    yellow = color_ratio(hsv, *YELLOW)
    return red, white, blue, yellow


def recognize_flag(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h = frame.shape[0]

    top = hsv[:h//2, :, :]
    bottom = hsv[h//2:, :, :]
    middle = hsv[h//3:2*h//3, :, :]

    r_top, w_top, b_top, y_top = dominant_colors(top)
    r_mid, w_mid, b_mid, y_mid = dominant_colors(middle)
    r_bot, w_bot, b_bot, y_bot = dominant_colors(bottom)

    if (w_top + y_top) > 0.30 and r_bot > 0.25:
        return "Poland"

    if b_top > 0.30 and y_bot > 0.30:
        return "Ukraine"

    if w_top > 0.20 and b_mid > 0.15 and r_bot > 0.20:
        return "Russia"

    return "Unknown"



cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not accessible")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    country = recognize_flag(frame)

    cv2.putText(
        frame,
        country,
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3,
        cv2.LINE_AA
    )

    cv2.imshow("Flag Recognition (Webcam)", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
