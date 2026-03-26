import cv2
import numpy as np
from src.detection.detector import ObjectDetector
from src.tracking.tracker import ObjectTracker

points = []

MARGIN = 35  # 🔥 FIXED


def select_points(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))


def select_lines(frame):
    global points
    points = []

    clone = frame.copy()

    cv2.namedWindow("Select Lines")
    cv2.setMouseCallback("Select Lines", select_points)

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
        return None, None

    return (points[0], points[1]), (points[2], points[3])


def distance_to_line(px, py, x1, y1, x2, y2):
    return abs((y2 - y1)*px - (x2 - x1)*py + x2*y1 - y2*x1) / (
        ((y2 - y1)**2 + (x2 - x1)**2) ** 0.5
    )


def process_video_stream(video_path, show=True, collect_metrics=False):
    detector = ObjectDetector("models/yolov8n.pt")
    tracker = ObjectTracker()

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("❌ Video not found")
        return None

    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read video")
        return None

    left_line, right_line = select_lines(frame)
    if left_line is None:
        return None

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    frame_count = 0
    paused = False

    object_positions = {}
    counted_in = set()
    counted_out = set()

    all_tracks = []
    crossing_events = []

    in_count = 0
    out_count = 0

    while True:

        if not paused:
            ret, frame = cap.read()
            if not ret:
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

            frame_data = {}

            if show:
                cv2.line(frame, left_line[0], left_line[1], (255, 0, 0), 3) # type: ignore
                cv2.line(frame, right_line[0], right_line[1], (0, 0, 255), 3) # type: ignore

            for track in tracks:
                x1, y1, x2, y2 = track["bbox"]
                track_id = track["id"]

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                frame_data[track_id] = (cx, cy)

                if show:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                if track_id in object_positions:
                    prev_y = object_positions[track_id][1]

                    # 🔵 IN
                    dist_left = distance_to_line(cx, cy, *left_line[0], *left_line[1])
                    if (
                        dist_left < MARGIN
                        and cy > prev_y
                        and track_id not in counted_in
                    ):
                        in_count += 1
                        counted_in.add(track_id)
                        crossing_events.append(("IN", frame_count))

                    # 🔴 OUT
                    dist_right = distance_to_line(cx, cy, *right_line[0], *right_line[1]) # type: ignore
                    if (
                        dist_right < MARGIN
                        and cy < prev_y
                        and track_id not in counted_out
                    ):
                        out_count += 1
                        counted_out.add(track_id)
                        crossing_events.append(("OUT", frame_count))

                object_positions[track_id] = (cx, cy)

            all_tracks.append(frame_data)

            if show:
                cv2.putText(frame, f"IN: {in_count}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
                cv2.putText(frame, f"OUT: {out_count}", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                cv2.imshow("Video", frame)

        key = cv2.waitKey(30) & 0xFF

        if key == ord('p'):
            paused = not paused

        if paused and key == ord('r'):
            new_lines = select_lines(frame)
            if new_lines[0] is not None:
                left_line, right_line = new_lines

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if collect_metrics:
        return {
            "tracks": all_tracks,
            "crossings": crossing_events,
            "in_count": in_count,
            "out_count": out_count
        }


def run_video_tracking():
    process_video_stream(
        video_path="data/input/test.mp4",
        show=True,
        collect_metrics=False
    )
