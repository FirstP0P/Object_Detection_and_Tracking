import cv2
from src.detection.detector import ObjectDetector


def run_image_detection():
    detector = ObjectDetector("models/yolov8n.pt")

    image_path = "data/input/test.jpg"
    frame = cv2.imread(image_path)

    if frame is None:
        print("❌ Image not found")
        return

    detections = detector.detect(frame)

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        conf = det["confidence"]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    output_path = "data/output/image_output.jpg"
    cv2.imwrite(output_path, frame)

    print(f"✅ Image detection saved at {output_path}")
