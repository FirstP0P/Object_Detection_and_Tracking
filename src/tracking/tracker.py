from sort import Sort
import numpy as np

class ObjectTracker:
    def __init__(self):
        self.tracker = Sort()

    def update(self, detections):
        """
        detections format:
        [[x1, y1, x2, y2, confidence], ...]
        """

        if len(detections) == 0:
            return []

        dets = np.array(detections)
        tracks = self.tracker.update(dets)

        results = []

        for track in tracks:
            x1, y1, x2, y2, track_id = track
            results.append({
                "bbox": (int(x1), int(y1), int(x2), int(y2)),
                "id": int(track_id)
            })

        return results
