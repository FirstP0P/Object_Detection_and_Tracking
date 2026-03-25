# 🚗 Object Detection & Tracking System with Vehicle Counting

## 📌 Overview

This project is a **real-time computer vision system** that performs:

* Object Detection using YOLOv8
* Object Tracking using SORT
* Direction-aware Vehicle Counting
* Interactive Line Selection (user-defined)
* Dynamic Line Adjustment during runtime

It is designed to simulate **real-world traffic monitoring systems** used in:

* Smart cities
* Surveillance systems
* Traffic analytics
* Autonomous systems

---

## 🎯 Features

* 🔍 Real-time object detection (YOLOv8)
* 🧠 Multi-object tracking with unique IDs (SORT)
* 📈 Vehicle counting (IN / OUT direction)
* 🖱️ Click-based dynamic line selection
* ⏸️ Pause & redraw lines during execution
* 🎥 Video input + output saving
* ⚡ Optimized performance (frame skipping)

---

## 🏗️ Project Structure

```
object_tracking_project/
│
├── data/
│   ├── input/
│   │   ├── test.jpg
│   │   └── test.mp4
│   └── output/
│
├── models/
│   └── yolov8n.pt
│
├── src/
│   ├── detection/
│   │   └── detector.py
│   │
│   ├── tracking/
│   │   └── tracker.py
│   │
│   ├── utils/
│   │   ├── draw_utils.py
│   │   └── video_utils.py
│   │
│   └── config/
│       └── config.py
│
├── sort.py
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ How the System Works

### 1️⃣ Object Detection (YOLOv8)

* Each frame is passed to a pretrained YOLOv8 model
* The model detects objects and returns:

  * Bounding boxes `(x1, y1, x2, y2)`
  * Confidence score
  * Class ID (car, person, etc.)

```
Frame → YOLO → Objects Detected
```

---

### 2️⃣ Object Tracking (SORT)

* Detected objects are passed to the SORT tracker
* SORT assigns a **unique ID** to each object
* IDs remain consistent across frames

```
Detections → SORT → Track IDs
```

---

### 3️⃣ Vehicle Counting Logic

* User defines **two lines** (left and right)
* Each tracked object has a **center point**
* When object crosses a line → count increases

#### Direction Detection:

* Moving down → IN count
* Moving up → OUT count

---

### 4️⃣ Dynamic Line Selection

* User clicks **4 points**:

  * 2 points → Left line (IN)
  * 2 points → Right line (OUT)

---

### 5️⃣ Interactive Controls

| Key | Action                     |
| --- | -------------------------- |
| `p` | Pause / Resume video       |
| `r` | Redraw lines (when paused) |
| `q` | Quit                       |

---

## 🧠 Technologies Used

* Python
* OpenCV
* YOLOv8 (Ultralytics)
* SORT (Simple Online Realtime Tracking)
* NumPy

---

## 🚀 Installation

### 1. Clone the repository

```bash
git https://github.com/FirstP0P/Object_Detection_and_Tracking.git
cd Object_Detection_and_Tracking
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Download YOLO model

```python
from ultralytics import YOLO
YOLO("yolov8n.pt")
```

Move the file to:

```
models/yolov8n.pt
```

---

### 4. Clone SORT

```bash
git clone https://github.com/abewley/sort.git
```

Copy `sort.py` into project root.

---

## ▶️ How to Run

```bash
python main.py
```

---

## 🎮 Choose Mode

```
1 → Image Detection
2 → Video Tracking
```

---

### 🖼️ Image Detection

* Input: `data/input/test.jpg`
* Output: `data/output/image_output.jpg`

---

### 🎥 Video Tracking

* Input: `data/input/test.mp4`
* Output: `data/output/output.mp4`

---

## 🖱️ Line Selection Instructions

1. A window will open
2. Click 4 points:

   * Point 1 & 2 → Left line (IN)
   * Point 3 & 4 → Right line (OUT)
3. Press `q` to confirm

---

## ⚡ Performance Optimizations

* Frame skipping (process every 3rd frame)
* Efficient tracking using SORT
* Optional frame resizing

---

## 📊 Output

* Bounding boxes with object IDs
* Vehicle counts displayed on screen
* Saved output video with overlays

---

## 🚀 Future Improvements

* Class-based filtering (cars only)
* Speed estimation
* Lane detection
* Web dashboard (Streamlit)
* Real-time webcam support

---

## 🏁 Conclusion

This project demonstrates a **complete computer vision pipeline**:

```
Detection → Tracking → Analytics
```

It combines AI models with real-world logic to build a **practical, scalable system**.
