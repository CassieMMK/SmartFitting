import os
import cv2
import numpy as np


class ClothingProcessor:

    def __init__(self):
        os.makedirs("assets/raw", exist_ok=True)
        os.makedirs("assets/processed", exist_ok=True)
        os.makedirs("assets/masks", exist_ok=True)

    def process(self, image_path, item_id):

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found")

        # 转HSV空间
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 假设背景是浅色（可调整）
        lower_bg = np.array([0, 0, 200])
        upper_bg = np.array([180, 40, 255])

        bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)

        # 反转得到衣服mask
        mask = cv2.bitwise_not(bg_mask)

        # 形态学操作去噪
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # 保存mask
        mask_path = f"assets/masks/{item_id}_mask.png"
        cv2.imwrite(mask_path, mask)

        # 生成透明背景图
        image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        image_rgba[:, :, 3] = mask

        processed_path = f"assets/processed/{item_id}_processed.png"
        cv2.imwrite(processed_path, image_rgba)

        return processed_path, mask_path
