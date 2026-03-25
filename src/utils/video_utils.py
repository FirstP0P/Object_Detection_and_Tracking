import cv2
from src.detection.detector import ObjectDetector
from src.tracking.tracker import ObjectTracker


def run_video_tracking():
    detector = ObjectDetector("models/yolov8n.pt")
    tracker = ObjectTracker()

    cap = cv2.VideoCapture("data/input/test.mp4")

    if not cap.isOpened():
        print("❌ Video not found")
        return

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

    out = cv2.VideoWriter(
        "data/output/output.mp4",
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("✅ Video ended")
            break

        frame_count += 1

        # 🔥 Speed optimization
        if frame_count % 3 != 0:
            continue

        # Optional resize (uncomment if needed)
        # frame = cv2.resize(frame, (640, 360))

        detections = detector.detect(frame)

        dets_for_sort = []
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            conf = det["confidence"]
            dets_for_sort.append([x1, y1, x2, y2, conf])

        tracks = tracker.update(dets_for_sort)

        for track in tracks:
            x1, y1, x2, y2 = track["bbox"]
            track_id = track["id"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        out.write(frame)
        cv2.imshow("Tracking", frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
