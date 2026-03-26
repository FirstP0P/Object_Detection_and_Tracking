# 🚗 Intelligent Object Detection, Tracking & Evaluation System

## 📌 Overview

This project is a **modular, real-time computer vision system** that performs:

* Object Detection using YOLOv8
* Multi-object Tracking using SORT
* Direction-aware Vehicle Counting (IN / OUT)
* Interactive Line Selection (dynamic + redraw support)
* Performance Evaluation (Temporal & Cycle Consistency)

It is designed to simulate **real-world traffic analytics systems** used in:

* Smart cities
* Surveillance systems
* Traffic monitoring
* Autonomous systems

---

## 🚀 Key Features

### 🔍 Core System

* Real-time object detection (YOLOv8)
* Persistent tracking with unique IDs (SORT)
* Direction-based vehicle counting (IN / OUT)
* Slanted / perspective-aware line crossing

---

### 🎮 Interactive Controls

* 🖱️ Click to define counting lines
* ⏸️ `p` → Pause / Resume video
* 🎯 `r` → Redraw lines (when paused)
* ❌ `q` → Quit

---

### ⚡ Performance Optimizations

* Frame skipping (process every 3rd frame)
* Track reuse for skipped frames
* Efficient single-pass pipeline

---

### 📊 Evaluation System

* Temporal Consistency (tracking stability)
* Cycle Consistency (system robustness)
* Counting metrics (IN / OUT / total crossings)

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
│   │   ├── video_utils.py                # Core pipeline
│   │   ├── performance_video_utils.py    # Evaluation (video)
│   │   └── performance_draw_utils.py     # Evaluation (image)
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

## ⚙️ System Architecture

### 🧠 Core Pipeline

```
Video → Detection (YOLOv8) → Tracking (SORT) → Line Crossing → Counting
```

---

### 🔄 Modular Design

```
process_video_stream()  ← Core Engine
        ↓
video_utils.py          → Visualization + Counting
performance_video_utils.py → Metrics (reuse same pipeline)
```

👉 Ensures:

* No duplicate logic
* Consistent evaluation
* Scalable architecture

---

## 🧠 How It Works

### 1️⃣ Object Detection (YOLOv8)

* Each frame is processed by YOLO
* Outputs:

  * Bounding boxes
  * Confidence scores
  * Class IDs

---

### 2️⃣ Object Tracking (SORT)

* Assigns unique IDs to objects
* Maintains identity across frames

---

### 3️⃣ Line Crossing Logic

* User defines 2 lines:

  * Left line → IN direction
  * Right line → OUT direction
* Uses:

  * Object center point
  * Distance-to-line + margin
  * Direction (movement)

---

### 4️⃣ Counting Logic

```
If object crosses line AND direction is correct AND not counted before
→ Increment count
```

✔ Uses margin (35 px) for robustness
✔ Prevents double counting

---

### 5️⃣ Performance Metrics

#### 📈 Temporal Consistency

* Measures smoothness of object motion
* Lower value = stable tracking

---

#### 🔄 Cycle Consistency

* Compares forward vs reversed tracking behavior
* Lower value = stable system

---

#### 🚗 Counting Metrics

* IN count
* OUT count
* Total crossings

---

## 🛠️ Installation

### 1. Clone repository

```bash
git clone https://github.com/FirstP0P/Object_Detection_and_Tracking.git
cd Object_Detection_and_Tracking
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Setup SORT

```bash
git clone https://github.com/abewley/sort.git
```

Copy `sort.py` to project root.

---

## ▶️ How to Run

```bash
python main.py
```

---

## 🎮 Menu Options

```
1 → Image Detection
2 → Video Tracking
3 → Video Performance Metrics
4 → Image Performance Metrics
0 → Exit
```

---

## 🖱️ Line Selection

#### Click 4 points:

   * Points 1–2 → Left line (IN)
   * Points 3–4 → Right line (OUT)


---

## 🎥 Video Controls

| Key | Action         |
| --- | -------------- |
| `p` | Pause / Resume |
| `r` | Redraw lines (when paused)   |
| `q` | Quit           |

---

## 📊 Output

### Visual Output

* Bounding boxes + IDs
* IN / OUT counters
* Dynamic line overlay

---

### Metrics Output

* Temporal consistency graph
* Cycle consistency graph
* Console metrics summary

---

## 🧠 Key Design Highlights

* ✔ Single-pass processing (efficient)
* ✔ Modular architecture (reusable core pipeline)
* ✔ Real-time interaction (pause + redraw)
* ✔ Robust counting (margin + direction + deduplication)
* ✔ Consistent evaluation (same pipeline reused)

---

## 🚀 Future Improvements

* Class-based filtering (cars only)
* IoU-based tracking accuracy
* Precision / Recall / mAP
* Speed estimation
* Lane detection
* Streamlit dashboard
* Real-time webcam support

---

## 🏁 Conclusion

This project goes beyond basic detection and implements a **complete AI pipeline**:

```
Detection → Tracking → Counting → Evaluation
```

It demonstrates:

* System design thinking
* Real-time processing
* Modular architecture
* Performance evaluation

---
