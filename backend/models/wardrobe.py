from backend.models.clothing_item import ClothingItem


class Wardrobe:

    def __init__(self):
        self.items = []

    def add_item(self, item: ClothingItem):
        self.items.append(item)

    def remove_item(self, item_id):
        self.items = [i for i in self.items if i.item_id != item_id]

    def get_by_category(self, category):
        return [i for i in self.items if i.category == category]

    def to_dict(self):
        return {
            "items": [item.to_dict() for item in self.items]
        }

    @staticmethod
    def from_dict(data):
        wardrobe = Wardrobe()
        for item_data in data.get("items", []):
            wardrobe.add_item(ClothingItem.from_dict(item_data))
        return wardrobe
