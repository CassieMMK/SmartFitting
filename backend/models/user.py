import uuid
from backend.models.identity import Identity


class User:

    def __init__(self, username, password, user_id=None):
        self.user_id = user_id or str(uuid.uuid4())
        self.username = username
        self.password = password  # MVP阶段明文存储
        self.identities = []

    def add_identity(self, identity: Identity):
        self.identities.append(identity)

    def get_identity(self, identity_id):
        for i in self.identities:
            if i.identity_id == identity_id:
                return i
        return None

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "identities": [i.to_dict() for i in self.identities]
        }

    @staticmethod
    def from_dict(data):
        user = User(
            username=data["username"],
            password=data["password"],
            user_id=data["user_id"]
        )
        for identity_data in data.get("identities", []):
            user.add_identity(Identity.from_dict(identity_data))
        return user
