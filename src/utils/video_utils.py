import cv2
from src.detection.detector import ObjectDetector
from src.tracking.tracker import ObjectTracker

# -------------------------------
# GLOBAL VARIABLES
# -------------------------------
points = []


# -------------------------------
# Mouse click
# -------------------------------
def select_points(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            print(f"Point selected: {(x, y)}")


# -------------------------------
# Distance from point to line
# -------------------------------
def distance_to_line(px, py, x1, y1, x2, y2):
    return abs((y2 - y1)*px - (x2 - x1)*py + x2*y1 - y2*x1) / (
        ((y2 - y1)**2 + (x2 - x1)**2) ** 0.5
    )


# -------------------------------
# LINE SELECTION FUNCTION
# -------------------------------
def select_lines(frame):
    global points
    points = []

    clone = frame.copy()

    cv2.namedWindow("Select Lines")
    cv2.setMouseCallback("Select Lines", select_points)

    print("\nClick 4 points:")
    print("1-2 → LEFT line (IN)")
    print("3-4 → RIGHT line (OUT)")
    print("Press 'q' when done")

    while True:
        temp = clone.copy()

        for p in points:
            cv2.circle(temp, p, 5, (0, 255, 0), -1)

        if len(points) >= 2:
            cv2.line(temp, points[0], points[1], (255, 0, 0), 2)
        if len(points) >= 4:
            cv2.line(temp, points[2], points[3], (0, 0, 255), 2)

        cv2.imshow("Select Lines", temp)

        key = cv2.waitKey(1)
        if key == ord('q') or len(points) == 4:
            break

    cv2.destroyWindow("Select Lines")

    if len(points) < 4:
        print("❌ Not enough points selected")
        return None, None

    return (points[0], points[1]), (points[2], points[3])


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def run_video_tracking():
    detector = ObjectDetector("models/yolov8n.pt")
    tracker = ObjectTracker()

    cap = cv2.VideoCapture("data/input/test.mp4")

    if not cap.isOpened():
        print("❌ Video not found")
        return

    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read video")
        return

    # Initial line selection
    left_line, right_line = select_lines(frame)
    if left_line is None:
        return

    # Reset video
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

    out = cv2.VideoWriter(
        "data/output/output.mp4",
        cv2.VideoWriter_fourcc(*'mp4v'), # type: ignore
        fps,
        (width, height)
    )

    frame_count = 0

    MARGIN = 35

    object_positions = {}
    in_count = 0
    out_count = 0

    counted_ids_in = set()
    counted_ids_out = set()

    paused = False

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("✅ Video ended")
                break

            frame_count += 1

            if frame_count % 3 != 0:
                continue

            detections = detector.detect(frame)

            dets_for_sort = []
            for det in detections:
                x1, y1, x2, y2 = det["bbox"]
                conf = det["confidence"]
                dets_for_sort.append([x1, y1, x2, y2, conf])

            tracks = tracker.update(dets_for_sort)

            # Draw lines
            cv2.line(frame, left_line[0], left_line[1], (255, 0, 0), 3)
            cv2.line(frame, right_line[0], right_line[1], (0, 0, 255), 3)  # type: ignore

            for track in tracks:
                x1, y1, x2, y2 = track["bbox"]
                track_id = track["id"]

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                # LEFT (IN)
                dist_left = distance_to_line(cx, cy, *left_line[0], *left_line[1])
                if dist_left < MARGIN and track_id not in counted_ids_in:
                    if track_id in object_positions:
                        if cy > object_positions[track_id][1]:
                            in_count += 1
                            counted_ids_in.add(track_id)

                # RIGHT (OUT)
                dist_right = distance_to_line(cx, cy, *right_line[0], *right_line[1]) # type: ignore
                if dist_right < MARGIN and track_id not in counted_ids_out:
                    if track_id in object_positions:
                        if cy < object_positions[track_id][1]:
                            out_count += 1
                            counted_ids_out.add(track_id)

                object_positions[track_id] = (cx, cy)

            cv2.putText(frame, f"IN: {in_count}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            cv2.putText(frame, f"OUT: {out_count}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            out.write(frame)
            cv2.imshow("Tracking + Counting", frame)

        key = cv2.waitKey(30) & 0xFF

        # 🔥 PAUSE
        if key == ord('p'):
            paused = not paused
            print("⏸ Paused" if paused else "▶ Resumed")

        # 🔥 REDRAW WHEN PAUSED
        if paused and key == ord('r'):
            print("🎯 Redrawing lines...")
            new_lines = select_lines(frame)
            if new_lines[0] is not None:
                left_line, right_line = new_lines

        if key == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
