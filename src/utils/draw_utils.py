import cv2
from src.detection.detector import ObjectDetector


def process_image(image_path, show=True, return_data=False):
    detector = ObjectDetector("models/yolov8n.pt")

    image = cv2.imread(image_path)

    if image is None:
        print("❌ Image not found")
        return None

    detections = detector.detect(image)

    results = []

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        conf = det["confidence"]
        class_id = det["class_id"]

        results.append(det)

        if show:
            cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(image, f"{class_id} {conf:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0,255,0), 2)

    if show:
        cv2.imshow("Image Detection", image)

        cv2.waitKey(1000)
        cv2.destroyAllWindows()

    if return_data:
        return {
            "detections": results,
            "image": image
        }


def run_image_detection():
    process_image(
        image_path="data/input/test.jpg",
        show=True,
        return_data=False
    )
