import uuid
from image_processing.clothing_processor import ClothingProcessor


def main():
    processor = ClothingProcessor()

    item_id = str(uuid.uuid4())

    processed_path, mask_path = processor.process(
        image_path="test.jpg",  # 你的测试图片
        item_id=item_id
    )

    print("Processed:", processed_path)
    print("Mask:", mask_path)


if __name__ == "__main__":
    main()
