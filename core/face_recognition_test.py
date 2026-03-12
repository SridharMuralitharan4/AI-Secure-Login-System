import face_recognition
import cv2
import os

dataset_path = "dataset/users"

known_encodings = []
known_names = []

for person in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person)

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)

        image = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            encoding = encodings[0]
            known_encodings.append(encoding)
            known_names.append(person)
        else:
            print("No face detected in:", image_path)