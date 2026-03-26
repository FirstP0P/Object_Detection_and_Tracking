import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from src.utils.video_utils import process_video_stream


def euclidean(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def run_video_performance():
    print("\n📊 Running Video Performance Evaluation...\n")

    # -------------------------------
    # CREATE TIMESTAMP FOLDER
    # -------------------------------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("data/output/video",timestamp)

    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------
    # RUN CORE PIPELINE
    # -------------------------------
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
    # TEMPORAL CONSISTENCY
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
    # CYCLE CONSISTENCY
    # -------------------------------
    reversed_tracks = list(reversed(all_tracks))

    cycle_scores = []

    for fwd_frame, bwd_frame in zip(all_tracks, reversed_tracks):
        diff = abs(len(fwd_frame) - len(bwd_frame))
        cycle_scores.append(diff)

    cycle_mean = np.mean(cycle_scores)

    # -------------------------------
    # PRINT RESULTS
    # -------------------------------
    print(f"📈 Temporal Consistency: {temporal_mean:.2f}")
    print(f"🔄 Cycle Consistency: {cycle_mean:.2f}")
    print(f"🚗 IN Count: {in_count}")
    print(f"🚗 OUT Count: {out_count}")
    print(f"📊 Total Crossings: {len(crossings)}")

    # -------------------------------
    # SAVE METRICS
    # -------------------------------
    metrics_path = os.path.join(output_dir, "video_metrics.txt")

    with open(metrics_path, "w") as f:
        f.write("Video Performance Metrics\n")
        f.write("=========================\n\n")
        f.write(f"Temporal Consistency: {temporal_mean:.2f}\n")
        f.write(f"Cycle Consistency   : {cycle_mean:.2f}\n\n")
        f.write(f"IN Count  : {in_count}\n")
        f.write(f"OUT Count : {out_count}\n")
        f.write(f"Total Crossings: {len(crossings)}\n")

    # -------------------------------
    # SAVE TEMPORAL GRAPH
    # -------------------------------
    temporal_graph_path = os.path.join(output_dir, "temporal_graph.png")

    plt.figure()
    plt.plot(temporal_scores)
    plt.title("Temporal Consistency")
    plt.xlabel("Frame")
    plt.ylabel("Movement")
    plt.savefig(temporal_graph_path)
    plt.close()

    # -------------------------------
    # SAVE CYCLE GRAPH
    # -------------------------------
    cycle_graph_path = os.path.join(output_dir, "cycle_graph.png")

    plt.figure()
    plt.plot(cycle_scores)
    plt.title("Cycle Consistency")
    plt.xlabel("Frame")
    plt.ylabel("Difference")
    plt.savefig(cycle_graph_path)
    plt.close()

    print(f"\n💾 All results saved in: {output_dir}")
    print("📁 Files:")
    print(" - video_metrics.txt")
    print(" - temporal_graph.png")
    print(" - cycle_graph.png")

    print("\n✅ Video evaluation completed\n")
