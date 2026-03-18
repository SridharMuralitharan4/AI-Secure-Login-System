import face_recognition
import cv2
import os

print("Program started...")

dataset_path = "dataset/users"

known_encodings = []
known_names = []

print("Loading dataset...")

for person in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person)
    images = os.listdir(person_folder)[:5]

    for image_name in images:
        image_path = os.path.join(person_folder, image_name)

        try:
            print("Processing:", image_path)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if len(encodings) > 0:
                known_encodings.append(encodings[0])
                known_names.append(person)

        except:
            pass

print("Dataset loaded:", len(known_names), "images")

video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Camera not detected")
    exit()

print("Starting camera...")

while True:
    ret, frame = video.read()

    if not ret:
        continue

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):

        matches = face_recognition.compare_faces(known_encodings, face_encoding)

        name = "Unknown"

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]

        top, right, bottom, left = [v * 4 for v in face_location]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) == 27:
        break

video.release()
cv2.destroyAllWindows()