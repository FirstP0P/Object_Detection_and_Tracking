from src.utils.draw_utils import run_image_detection
from src.utils.video_utils import run_video_tracking

if __name__ == "__main__":
    print("\nSelect Mode:")
    print("1 → Image Detection")
    print("2 → Video Tracking")

    choice = input("Enter choice (1/2): ")

    if choice == "1":
        run_image_detection()
    elif choice == "2":
        run_video_tracking()
    else:
        print("❌ Invalid choice")
