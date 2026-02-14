from models.user import User
from models.identity import Identity
from models.clothing_item import ClothingItem
from storage.database import load_users, save_users


def main():

    users = load_users()

    # 创建新用户
    user = User("cassie", "123456")

    # 创建身份
    identity = Identity(
        nickname="Cassie",
        gender="female",
        age=20,
        style_preference="casual",
        job_type="student",
        personality="outgoing"
    )

    # 添加衣服
    item1 = ClothingItem(
        name="White T-shirt",
        category="tops",
        color="white",
        style="casual",
        season="summer"
    )

    item2 = ClothingItem(
        name="Blue Jeans",
        category="bottoms",
        color="blue",
        style="casual",
        season="all"
    )

    identity.wardrobe.add_item(item1)
    identity.wardrobe.add_item(item2)

    user.add_identity(identity)

    users.append(user)

    save_users(users)

    print("User saved successfully.")


if __name__ == "__main__":
    main()
