import json
import os
from models.user import User


DATA_PATH = "data/users.json"


def load_users():
    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [User.from_dict(u) for u in data]


def save_users(users):
    os.makedirs("data", exist_ok=True)

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in users], f, indent=4, ensure_ascii=False)
