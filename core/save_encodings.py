import face_recognition
import os
import pickle

dataset_path = "dataset/users"

known_encodings = []
known_names = []

for person in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person)
    images = os.listdir(person_folder)[:5]

    for image_name in images:
        image_path = os.path.join(person_folder, image_name)

        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if len(encodings) > 0:
                known_encodings.append(encodings[0])
                known_names.append(person)
        except:
            pass

data = {"encodings": known_encodings, "names": known_names}

with open("encodings.pkl", "wb") as f:
    pickle.dump(data, f)

print("Encodings saved")