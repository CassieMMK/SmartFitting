import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request
from collections import deque
import numpy as np

# ============================
# 下载模型
# ============================

POSE_MODEL = "pose_landmarker_lite.task"
FACE_MODEL = "face_landmarker.task"

def download(url, name):
    if not os.path.exists(name):
        print("Downloading", name)
        urllib.request.urlretrieve(url, name)

download(
    "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite.task",
    POSE_MODEL
)

download(
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker.task",
    FACE_MODEL
)

# ============================
# Pose
# ============================

BaseOptions = python.BaseOptions
VisionRunningMode = vision.RunningMode
PoseLandmarker = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions

pose_result = None

def pose_callback(result, output, ts):
    global pose_result
    pose_result = result

pose_options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=POSE_MODEL),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=pose_callback
)

pose_detector = PoseLandmarker.create_from_options(pose_options)

# ============================
# Face
# ============================

FaceLandmarker = vision.FaceLandmarker
FaceLandmarkerOptions = vision.FaceLandmarkerOptions

face_result = None

def face_callback(result, output, ts):
    global face_result
    face_result = result

face_options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=FACE_MODEL),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=face_callback,
    output_face_blendshapes=True,
    num_faces=1
)

face_detector = FaceLandmarker.create_from_options(face_options)

# ============================
# 情绪系统升级
# ============================

emotion_buffer = deque(maxlen=60)
trend_buffer = deque(maxlen=30)

baseline = None
baseline_frames = 60
baseline_data = []

prev_features = None


def extract_features(blendshapes):
    data = {}
    for bs in blendshapes:
        data[bs.category_name] = bs.score
    return data


def compute_baseline():
    global baseline
    keys = baseline_data[0].keys()
    baseline = {}
    for k in keys:
        baseline[k] = np.mean([f[k] for f in baseline_data])


def compute_delta(features):
    delta = {}
    for k in baseline:
        delta[k] = features.get(k, 0) - baseline.get(k, 0)
    return delta


def compute_satisfaction(delta, velocity):

    smile = delta.get("mouthSmileLeft", 0) + delta.get("mouthSmileRight", 0)
    frown = delta.get("browDownLeft", 0) + delta.get("browDownRight", 0)
    press = delta.get("mouthPressLeft", 0) + delta.get("mouthPressRight", 0)
    squint = delta.get("eyeSquintLeft", 0) + delta.get("eyeSquintRight", 0)
    eye_open = delta.get("eyeWideLeft", 0) + delta.get("eyeWideRight", 0)

    smile_v = velocity.get("mouthSmileLeft", 0) + velocity.get("mouthSmileRight", 0)

    score = (
        0.5 * smile
        - 0.3 * frown
        - 0.2 * press
        - 0.2 * squint
        + 0.2 * eye_open
        + 0.3 * smile_v
    )

    return float(np.clip(score, -1, 1))


def compute_velocity(current):
    global prev_features
    if prev_features is None:
        prev_features = current
        return {}

    velocity = {}
    for k in current:
        velocity[k] = current[k] - prev_features.get(k, 0)

    prev_features = current
    return velocity


def compute_trend():
    if len(trend_buffer) < 10:
        return 0

    y = np.array(trend_buffer)
    x = np.arange(len(y))

    slope = np.polyfit(x, y, 1)[0]
    return slope


# ============================
# 摄像头
# ============================

cap = cv2.VideoCapture(0)
timestamp = 0

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame
    )

    pose_detector.detect_async(mp_image, timestamp)
    face_detector.detect_async(mp_image, timestamp)

    # ---------- Face ----------
    if face_result and face_result.face_blendshapes:

        features = extract_features(face_result.face_blendshapes[0])

        # ===== 建立 baseline =====
        if baseline is None:
            baseline_data.append(features)

            cv2.putText(
                frame, "Calibrating baseline...",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,(0,255,255),2
            )

            if len(baseline_data) >= baseline_frames:
                compute_baseline()

        else:
            delta = compute_delta(features)
            velocity = compute_velocity(features)

            score = compute_satisfaction(delta, velocity)

            trend_buffer.append(score)
            slope = compute_trend()

            txt = f"Satisfaction: {score:.2f}"
            trend_txt = f"Trend: {slope:.4f}"

            cv2.putText(frame, txt,
                        (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(0,255,255),2)

            cv2.putText(frame, trend_txt,
                        (20,80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,(0,255,0),2)

    cv2.imshow("Pose + Face + Emotion V2", frame)

    timestamp += 1

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
