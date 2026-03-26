import cv2
import matplotlib.pyplot as plt
from src.detection.detector import ObjectDetector


# -------------------------------
# IMAGE PERFORMANCE (AUGMENTATION)
# -------------------------------
def run_image_performance():
    print("\n🖼️ Running Image Performance Analysis...\n")

    detector = ObjectDetector("models/yolov8n.pt")

    image_path = "data/input/test.jpg"

    image = cv2.imread(image_path)

    if image is None:
        print("❌ Image not found")
        return

    # -------------------------------
    # AUGMENTATIONS
    # -------------------------------
    flipped = cv2.flip(image, 1)
    bright = cv2.convertScaleAbs(image, alpha=1.2, beta=30)

    # -------------------------------
    # DETECTIONS
    # -------------------------------
    det_orig = detector.detect(image)
    det_flip = detector.detect(flipped)
    det_bright = detector.detect(bright)

    counts = [len(det_orig), len(det_flip), len(det_bright)]

    print("Detection Counts:")
    print(f"Original: {counts[0]}")
    print(f"Flipped : {counts[1]}")
    print(f"Bright  : {counts[2]}")

    # -------------------------------
    # VISUALIZATION
    # -------------------------------
    plt.bar(["Original", "Flipped", "Bright"], counts)
    plt.title("Augmentation Consistency (Image)")
    plt.ylabel("Detections")
    plt.show()

    print("\n✅ Image metrics computed successfully\n")
