import cv2
import dlib
import face_recognition
import pickle
import random
import time
from scipy.spatial import distance

with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

cap = cv2.VideoCapture(0)

challenges = random.sample(["BLINK", "LEFT", "RIGHT"], 2)
current_step = 0

blink_count = 0
counter = 0
prev_x = None

EYE_THRESHOLD = 0.25
FRAME_CHECK = 2

start_time = time.time()
TIME_LIMIT = 5

process_this_frame = True
name = "Unknown"

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    display_frame = frame.copy()

    if process_this_frame:

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        if len(face_encodings) > 0:
            matches = face_recognition.compare_faces(known_encodings, face_encodings[0])
            if True in matches:
                name = known_names[matches.index(True)]
            else:
                name = "Unknown"

    process_this_frame = not process_this_frame

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) != 1:
        cv2.putText(display_frame, "ONLY ONE PERSON", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.imshow("Final AI Secure Login", display_frame)
        cv2.waitKey(1500)
        break

    if time.time() - start_time > TIME_LIMIT:
        cv2.putText(display_frame, "TIME OUT - FAKE", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.imshow("Final AI Secure Login", display_frame)
        cv2.waitKey(1500)
        break

    face = faces[0]
    landmarks = predictor(gray, face)

    left_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36,42)]
    right_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42,48)]

    ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

    if ear < EYE_THRESHOLD:
        counter += 1
    else:
        if counter >= FRAME_CHECK:
            blink_count += 1
        counter = 0

    nose_x = landmarks.part(30).x

    moved_left = False
    moved_right = False

    if prev_x is not None:
        if nose_x - prev_x > 10:
            moved_right = True
        elif prev_x - nose_x > 10:
            moved_left = True

    prev_x = nose_x

    if current_step < len(challenges):
        current = challenges[current_step]

        if current == "BLINK" and blink_count >= 1:
            current_step += 1
            blink_count = 0
            start_time = time.time()

        elif current == "LEFT" and moved_left:
            current_step += 1
            start_time = time.time()

        elif current == "RIGHT" and moved_right:
            current_step += 1
            start_time = time.time()

    if current_step == len(challenges) and name != "Unknown":
        cv2.putText(display_frame, "ACCESS GRANTED: " + name, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        with open("logs.txt", "a") as f:
            f.write(name + " logged in at " + time.strftime("%H:%M:%S") + "\n")

        cv2.imshow("Final AI Secure Login", display_frame)
        cv2.waitKey(1500)
        break

    elif current_step == len(challenges) and name == "Unknown":
        cv2.putText(display_frame, "FAKE USER", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.imshow("Final AI Secure Login", display_frame)
        cv2.waitKey(1500)
        break

    if current_step < len(challenges):
        text = "Do: " + challenges[current_step]
    else:
        text = "DONE"

    cv2.putText(display_frame, text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.imshow("Final AI Secure Login", display_frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()