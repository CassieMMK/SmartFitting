import os
import cv2
import numpy as np
from PIL import Image
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class ClothingProcessor:

    def __init__(self):

        os.makedirs("assets/raw", exist_ok=True)
        os.makedirs("assets/processed", exist_ok=True)
        os.makedirs("assets/masks", exist_ok=True)

        # 下载模型（如果不存在）
        model_path = "selfie_segmenter.tflite"
        if not os.path.exists(model_path):
            import urllib.request
            url = "https://storage.googleapis.com/mediapipe-assets/selfie_segmenter.tflite"
            urllib.request.urlretrieve(url, model_path)

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.ImageSegmenterOptions(
            base_options=base_options,
            output_category_mask=True
        )

        self.segmenter = vision.ImageSegmenter.create_from_options(options)

    def process(self, image_path, item_id):

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found.")

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )

        segmentation_result = self.segmenter.segment(mp_image)

        category_mask = segmentation_result.category_mask.numpy_view()

        # 前景为1，背景为0
        binary_mask = np.where(category_mask > 0, 255, 0).astype(np.uint8)

        mask_path = f"assets/masks/{item_id}_mask.png"
        cv2.imwrite(mask_path, binary_mask)

        image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        image_rgba[:, :, 3] = binary_mask

        processed_path = f"assets/processed/{item_id}_processed.png"
        cv2.imwrite(processed_path, image_rgba)

        return processed_path, mask_path
