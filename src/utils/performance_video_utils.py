import numpy as np
import matplotlib.pyplot as plt
from src.utils.video_utils import process_video_stream


def euclidean(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def run_video_performance():
    print("\n📊 Running Performance Evaluation...\n")

    data = process_video_stream(
        video_path="data/input/test.mp4",
        show=True,
        collect_metrics=True
    )

    if data is None:
        return

    all_tracks = data["tracks"]
    crossings = data["crossings"]
    in_count = data["in_count"]
    out_count = data["out_count"]

    # -------------------------------
    # 1️⃣ TEMPORAL CONSISTENCY
    # -------------------------------
    temporal_scores = []

    for i in range(1, len(all_tracks)):
        prev_frame = all_tracks[i - 1]
        curr_frame = all_tracks[i]

        dists = []

        for track_id in curr_frame:
            if track_id in prev_frame:
                dists.append(
                    euclidean(curr_frame[track_id], prev_frame[track_id])
                )

        if dists:
            temporal_scores.append(np.mean(dists))

    temporal_mean = np.mean(temporal_scores)

    # -------------------------------
    # 2️⃣ CYCLE CONSISTENCY
    # -------------------------------
    reversed_tracks = list(reversed(all_tracks))

    cycle_scores = []

    for fwd_frame, bwd_frame in zip(all_tracks, reversed_tracks):
        # Compare number of tracked objects
        diff = abs(len(fwd_frame) - len(bwd_frame))
        cycle_scores.append(diff)

    cycle_mean = np.mean(cycle_scores)

    # -------------------------------
    # PRINT RESULTS
    # -------------------------------
    print(f"📈 Temporal Consistency: {temporal_mean:.2f} (lower is better)")
    print(f"🔄 Cycle Consistency: {cycle_mean:.2f} (lower is better)")
    print(f"🚗 IN Count: {in_count}")
    print(f"🚗 OUT Count: {out_count}")
    print(f"📊 Total Crossings: {len(crossings)}")

    # -------------------------------
    # VISUALIZATION
    # -------------------------------
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(temporal_scores)
    plt.title("Temporal Consistency")
    plt.xlabel("Frame")
    plt.ylabel("Movement")

    plt.subplot(1, 2, 2)
    plt.plot(cycle_scores)
    plt.title("Cycle Consistency")
    plt.xlabel("Frame")
    plt.ylabel("Difference")

    plt.tight_layout()
    plt.show()
