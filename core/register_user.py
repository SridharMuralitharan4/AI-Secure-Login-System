import cv2
import os
import time

import sys

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input("Enter user name: ")

dataset_path = f"dataset/users/{name}"
os.makedirs(dataset_path, exist_ok=True)

cap = cv2.VideoCapture(0)

print("Look at the camera. Capturing images...")

count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Register Face", frame)

    # save image every 0.15 sec
    if time.time() - start_time > count * 0.15:
        img_path = f"{dataset_path}/{count}.jpg"
        cv2.imwrite(img_path, frame)
        count += 1

    if count >= 20:
        break

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

print("Registration complete.")
import subprocess
subprocess.run(["venv\\Scripts\\python", "core\\save_encodings.py"])