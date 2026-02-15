from backend.models.wardrobe import Wardrobe
import uuid


class Identity:

    def __init__(
        self,
        nickname,
        gender,
        age,
        style_preference=None,
        job_type=None,
        personality=None,
        identity_id=None
    ):
        self.identity_id = identity_id or str(uuid.uuid4())
        self.nickname = nickname
        self.gender = gender
        self.age = age
        self.style_preference = style_preference
        self.job_type = job_type
        self.personality = personality

        self.wardrobe = Wardrobe()

    def to_dict(self):
        return {
            "identity_id": self.identity_id,
            "nickname": self.nickname,
            "gender": self.gender,
            "age": self.age,
            "style_preference": self.style_preference,
            "job_type": self.job_type,
            "personality": self.personality,
            "wardrobe": self.wardrobe.to_dict()
        }

    @staticmethod
    def from_dict(data):
        identity = Identity(
            nickname=data["nickname"],
            gender=data["gender"],
            age=data["age"],
            style_preference=data.get("style_preference"),
            job_type=data.get("job_type"),
            personality=data.get("personality"),
            identity_id=data["identity_id"]
        )

        identity.wardrobe = Wardrobe.from_dict(data["wardrobe"])
        return identity
