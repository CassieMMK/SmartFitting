import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request


# =============================
# 下载模型
# =============================

MODEL_PATH = "pose_landmarker_lite.task"

if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
    urllib.request.urlretrieve(url, MODEL_PATH)


# =============================
# 配置
# =============================

BaseOptions = python.BaseOptions
PoseLandmarker = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions
VisionRunningMode = vision.RunningMode


pose_result = None


def result_callback(result, output_image, timestamp_ms):
    global pose_result
    pose_result = result


options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=result_callback
)

detector = PoseLandmarker.create_from_options(options)


# =============================
# 骨架连接表（官方定义）
# =============================

POSE_CONNECTIONS = [
    (11, 13), (13, 15),  # left arm
    (12, 14), (14, 16),  # right arm
    (11, 12),           # shoulders
    (11, 23), (12, 24), # torso
    (23, 24),           # hips
    (23, 25), (25, 27), (27, 29), (29, 31),  # left leg
    (24, 26), (26, 28), (28, 30), (30, 32),  # right leg
    (0, 1), (0, 2), (1, 3), (2, 4)           # head
]


# =============================
# 打开摄像头
# =============================

cap = cv2.VideoCapture(0)
timestamp = 0


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if not ret:
        break

    h, w, _ = frame.shape

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame
    )

    detector.detect_async(mp_image, timestamp)

    # 画骨架
    if pose_result and pose_result.pose_landmarks:

        for landmarks in pose_result.pose_landmarks:

            points = []

            for lm in landmarks:
                x = int(lm.x * w)
                y = int(lm.y * h)
                points.append((x, y))

                cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

            for start, end in POSE_CONNECTIONS:
                if start < len(points) and end < len(points):
                    cv2.line(
                        frame,
                        points[start],
                        points[end],
                        (255, 0, 0),
                        2
                    )

    cv2.imshow("Pose Detection", frame)

    timestamp += 1

    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
