import requests

TRYON_URL = "http://localhost:8001/tryon"

def request_tryon(user_image_path, cloth_image_path):

    with open(user_image_path, "rb") as user_img, \
         open(cloth_image_path, "rb") as cloth_img:

        response = requests.post(
            TRYON_URL,
            files={
                "model_image": user_img,
                "cloth_image": cloth_img
            }
        )

    return response.json()