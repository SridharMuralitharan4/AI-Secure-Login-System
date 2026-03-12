import cv2
import os

name = input("Enter user name: ")

dataset_path = f"dataset/users/{name}"
os.makedirs(dataset_path, exist_ok=True)

cap = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = cap.read()

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        img_path = f"{dataset_path}/{count}.jpg"
        cv2.imwrite(img_path, frame)
        print("Image saved:", img_path)
        count += 1

    if key == 27 or count >= 20:
        break

cap.release()
cv2.destroyAllWindows()