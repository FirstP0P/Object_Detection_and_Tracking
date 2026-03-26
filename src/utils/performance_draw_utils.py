import cv2
import matplotlib.pyplot as plt
from src.utils.draw_utils import process_image


def run_image_performance():
    print("\n🖼️ Running Image Performance Evaluation...\n")

    image_path = "data/input/test.jpg"

    # Original
    original_data = process_image(
        image_path=image_path,
        show=False,
        return_data=True
    )

    if original_data is None:
        return

    original_img = original_data["image"]
    det_orig = original_data["detections"]

    # Augmentations
    flipped = cv2.flip(original_img, 1)
    bright = cv2.convertScaleAbs(original_img, alpha=1.2, beta=30)

    # Save temp images (simple reuse)
    cv2.imwrite("temp_flip.jpg", flipped)
    cv2.imwrite("temp_bright.jpg", bright)

    flip_data = process_image("temp_flip.jpg", show=False, return_data=True)
    bright_data = process_image("temp_bright.jpg", show=False, return_data=True)

    det_flip = flip_data["detections"]
    det_bright = bright_data["detections"]

    counts = [len(det_orig), len(det_flip), len(det_bright)]

    print("📊 Detection Counts:")
    print(f"Original: {counts[0]}")
    print(f"Flipped : {counts[1]}")
    print(f"Bright  : {counts[2]}")

    # Graph
    plt.bar(["Original", "Flipped", "Bright"], counts)
    plt.title("Augmentation Consistency")
    plt.ylabel("Detections")
    plt.show()
