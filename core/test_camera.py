import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not detected")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Camera Test", frame)

    # stop if ESC is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

    # stop if window is closed manually
    if cv2.getWindowProperty("Camera Test", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()