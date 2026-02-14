import uuid


class ClothingItem:

    def __init__(
        self,
        name,
        category,
        color,
        style,
        season,
        image_path=None,
        item_id=None
    ):
        self.item_id = item_id or str(uuid.uuid4())
        self.name = name
        self.category = category  # tops, bottoms, shoes, etc.
        self.color = color
        self.style = style
        self.season = season
        self.image_path = image_path

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "category": self.category,
            "color": self.color,
            "style": self.style,
            "season": self.season,
            "image_path": self.image_path
        }

    @staticmethod
    def from_dict(data):
        return ClothingItem(
            name=data["name"],
            category=data["category"],
            color=data["color"],
            style=data["style"],
            season=data["season"],
            image_path=data.get("image_path"),
            item_id=data["item_id"]
        )
