import cv2
import os
from datetime import datetime
import matplotlib.pyplot as plt
from src.utils.draw_utils import process_image


def run_image_performance():
    print("\n🖼️ Running Image Performance Evaluation...\n")

    image_path = "data/input/test.jpg"

    # -------------------------------
    # CREATE TIMESTAMP FOLDER
    # -------------------------------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("data/output/image", timestamp)

    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------
    # ORIGINAL IMAGE
    # -------------------------------
    original_data = process_image(
        image_path=image_path,
        show=False,
        return_data=True
    )

    if original_data is None:
        return

    original_img = original_data["image"]
    det_orig = original_data["detections"]

    # Save original
    original_path = os.path.join(output_dir, "original.jpg")
    cv2.imwrite(original_path, original_img)

    # -------------------------------
    # AUGMENTATIONS
    # -------------------------------
    flipped = cv2.flip(original_img, 1)
    bright = cv2.convertScaleAbs(original_img, alpha=1.2, beta=30)

    flip_path = os.path.join(output_dir, "flipped.jpg")
    bright_path = os.path.join(output_dir, "bright.jpg")

    cv2.imwrite(flip_path, flipped)
    cv2.imwrite(bright_path, bright)

    # -------------------------------
    # DETECTIONS (REUSE PIPELINE)
    # -------------------------------
    flip_data = process_image(flip_path, show=False, return_data=True)
    bright_data = process_image(bright_path, show=False, return_data=True)

    det_flip = flip_data["detections"] # type: ignore
    det_bright = bright_data["detections"] # type: ignore

    # -------------------------------
    # METRICS
    # -------------------------------
    counts = [len(det_orig), len(det_flip), len(det_bright)]

    print("📊 Detection Counts:")
    print(f"Original: {counts[0]}")
    print(f"Flipped : {counts[1]}")
    print(f"Bright  : {counts[2]}")

    # -------------------------------
    # SAVE METRICS
    # -------------------------------
    metrics_path = os.path.join(output_dir, "metrics.txt")

    with open(metrics_path, "w") as f:
        f.write("Image Performance Metrics\n")
        f.write("=========================\n\n")
        f.write(f"Original Detections: {counts[0]}\n")
        f.write(f"Flipped Detections : {counts[1]}\n")
        f.write(f"Bright Detections  : {counts[2]}\n")

    # -------------------------------
    # SAVE GRAPH
    # -------------------------------
    graph_path = os.path.join(output_dir, "graph.png")

    plt.bar(["Original", "Flipped", "Bright"], counts)
    plt.title("Augmentation Consistency")
    plt.ylabel("Detections")
    plt.savefig(graph_path)
    plt.close()

    print(f"\n💾 All results saved in: {output_dir}")
    print("📁 Files:")
    print(" - original.jpg")
    print(" - flipped.jpg")
    print(" - bright.jpg")
    print(" - metrics.txt")
    print(" - graph.png")

    print("\n✅ Image evaluation completed\n")
