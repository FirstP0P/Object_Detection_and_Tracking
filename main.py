from src.utils.draw_utils import run_image_detection
from src.utils.video_utils import run_video_tracking
from src.utils.performance_video_utils import run_video_performance
from src.utils.performance_draw_utils import run_image_performance

def main():
    while True:
        print("\n========== MENU ==========")
        print("1 → Image Detection")
        print("2 → Video Tracking")
        print("3 → Image Performance Metrics")
        print("4 → Video Performance Metrics")
        print("0 → Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            run_image_detection()

        elif choice == "2":
            run_video_tracking()

        elif choice == "3":
            run_image_performance()

        elif choice == "4":
            run_video_performance()

        elif choice == "0":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
