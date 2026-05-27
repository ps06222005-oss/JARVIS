import cv2
import mediapipe as mp
from ultralytics import YOLO
import ollama
import time

# =========================
# LOAD YOLO MODEL
# =========================
model = YOLO("yolov8n.pt")

# =========================
# MEDIAPIPE HANDS
# =========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# =========================
# FACE DETECTION
# =========================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

# =========================
# START CAMERA
# =========================
cam = cv2.VideoCapture(0)

# =========================
# AI ANALYSIS TIMER
# =========================
last_analysis = time.time()

print("JARVIS Vision Started...")

while True:

    ret, frame = cam.read()

    if not ret:
        break

    # =========================
    # FACE DETECTION
    # =========================
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        1.1,
        4
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            "Face",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )

    # =========================
    # HAND TRACKING
    # =========================
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # =========================
    # OBJECT DETECTION
    # =========================
    detections = model(frame)

    annotated_frame = detections[0].plot()

    # =========================
    # AI IMAGE ANALYSIS
    # EVERY 15 SECONDS
    # =========================
    current_time = time.time()

    if current_time - last_analysis > 15:

        image_path = "vision_capture.jpg"

        cv2.imwrite(image_path, frame)

        try:

            response = ollama.chat(
                model='llava',
                messages=[
                    {
                        'role': 'user',
                        'content': 'Describe what you see.',
                        'images': [image_path]
                    }
                ]
            )

            print("\nAI Vision:")
            print(response['message']['content'])
            print()

        except Exception as e:
            print("AI Vision Error:", e)

        last_analysis = current_time

    # =========================
    # DISPLAY
    # =========================
    cv2.imshow(
        "JARVIS Vision",
        annotated_frame
    )

    # =========================
    # EXIT
    # =========================
    key = cv2.waitKey(1)

    if key == 27:
        break

# =========================
# CLEANUP
# =========================
cam.release()
cv2.destroyAllWindows()