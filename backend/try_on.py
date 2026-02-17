import cv2
import numpy as np
import mediapipe as mp


class TryOnEngine:

    def __init__(self, clothing_path):
        self.clothing_img = cv2.imread(clothing_path, cv2.IMREAD_UNCHANGED)

        if self.clothing_img is None:
            raise ValueError("Clothing image not found")

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

    def overlay_clothing(self, frame):

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        if not results.pose_landmarks:
            return frame

        landmarks = results.pose_landmarks.landmark

        h, w, _ = frame.shape

        # 获取肩膀关键点
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]

        x1, y1 = int(left_shoulder.x * w), int(left_shoulder.y * h)
        x2, y2 = int(right_shoulder.x * w), int(right_shoulder.y * h)

        shoulder_width = abs(x2 - x1)

        if shoulder_width < 10:
            return frame

        # 缩放衣服
        clothing_h, clothing_w = self.clothing_img.shape[:2]
        scale = shoulder_width / clothing_w * 1.5

        new_w = int(clothing_w * scale)
        new_h = int(clothing_h * scale)

        resized = cv2.resize(self.clothing_img, (new_w, new_h))

        # 贴图位置
        center_x = int((x1 + x2) / 2)
        top_y = int(min(y1, y2) - new_h * 0.3)

        x_start = center_x - new_w // 2
        y_start = top_y

        return self.paste_transparent(frame, resized, x_start, y_start)

    def paste_transparent(self, background, overlay, x, y):

        bh, bw = background.shape[:2]
        oh, ow = overlay.shape[:2]

        if x < 0:
            overlay = overlay[:, -x:]
            ow = overlay.shape[1]
            x = 0

        if y < 0:
            overlay = overlay[-y:, :]
            oh = overlay.shape[0]
            y = 0

        if x + ow > bw:
            overlay = overlay[:, :bw - x]
            ow = overlay.shape[1]

        if y + oh > bh:
            overlay = overlay[:bh - y, :]
            oh = overlay.shape[0]

        if overlay.shape[2] < 4:
            return background

        alpha = overlay[:, :, 3] / 255.0
        for c in range(3):
            background[y:y+oh, x:x+ow, c] = (
                alpha * overlay[:, :, c] +
                (1 - alpha) * background[y:y+oh, x:x+ow, c]
            )

        return background


def main():

    clothing_path = "assets/processed/sample_processed.png"
    engine = TryOnEngine(clothing_path)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        output = engine.overlay_clothing(frame)

        cv2.imshow("Smart Try-On", output)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
 