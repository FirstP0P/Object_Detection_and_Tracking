# 🚗 Intelligent Object Detection, Tracking & Evaluation System

## 📌 Overview

This project is a **modular, real-time computer vision system** that performs:

* Object Detection using YOLOv8
* Multi-object Tracking using SORT
* Direction-aware Vehicle Counting (IN / OUT)
* Interactive Line Selection (dynamic + redraw support)
* Performance Evaluation (Temporal & Cycle Consistency)
* Experiment Logging (timestamp-based output storage)

It simulates **real-world traffic analytics systems** used in:

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
* Perspective-aware line crossing (custom slanted lines)

---

### 🎮 Interactive Controls

* 🖱️ Click to define lines
* ⏸️ `p` → Pause / Resume
* 🎯 `r` → Redraw lines
* ❌ `q` → Quit

---

### ⚡ Performance Optimizations

* Frame skipping (process every 3rd frame)
* Track reuse for skipped frames
* Single-pass pipeline (efficient)

---

### 📊 Evaluation System

#### Video Metrics

* 📈 Temporal Consistency (tracking stability)
* 🔄 Cycle Consistency (system robustness)
* 🚗 IN / OUT counting metrics

#### Image Metrics

* Augmentation Consistency (robustness under transformations)

---

### 💾 Experiment Logging

Outputs are **organized by type and timestamp**:

```text
data/output/
├── image/
│   └── 20260326_150210/
│       ├── original.jpg
│       ├── flipped.jpg
│       ├── bright.jpg
│       ├── metrics.txt
│       └── graph.png
│
└── video/
    └── 20260326_150305/
        ├── video_metrics.txt
        ├── temporal_graph.png
        └── cycle_graph.png
```

✔ Separate folders for image & video
✔ Timestamp-based runs
✔ No overwriting
✔ Fully reproducible

---

## 🏗️ Project Structure

```
object_tracking_project/
│
├── data/
│   ├── input/
│   │   ├── test.jpg
│   │   └── test.mp4
│   │
│   └── output/
│       ├── image/     # Image evaluation outputs
│       └── video/     # Video evaluation outputs
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
│   │   ├── video_utils.py
│   │   ├── performance_draw_utils.py
│   │   └── performance_video_utils.py
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

### 🧠 Core Pipelines

#### Video Pipeline

```
Video → Detection → Tracking → Line Crossing → Counting
```

#### Image Pipeline

```
Image → Detection → Augmentation → Evaluation
```

---

### 🔄 Modular Design

```
process_video_stream()  → core engine (video)
process_image()         → core engine (image)

↓ reused by ↓

video_utils.py                → visualization
performance_video_utils.py    → evaluation

draw_utils.py                 → detection
performance_draw_utils.py     → evaluation
```

✔ No duplicated logic
✔ Consistent evaluation
✔ Scalable architecture

---

## 🧠 How It Works

### 1️⃣ Detection (YOLOv8)

* Processes image/frame
* Outputs bounding boxes, confidence, class

---

### 2️⃣ Tracking (SORT)

* Assigns unique IDs
* Maintains identity across frames

---

### 3️⃣ Line Crossing Logic

* User defines 2 lines:

  * Left → IN
  * Right → OUT
* Uses:

  * Object center
  * Distance-to-line
  * Direction (movement)
  * Margin (35 px)

---

### 4️⃣ Counting Logic

```
If object crosses line AND direction is correct AND not counted before
→ Count increment
```

✔ Prevents double counting
✔ Robust to noise

---

### 5️⃣ Performance Metrics

#### 📈 Temporal Consistency

* Measures motion smoothness
* Lower = better tracking

#### 🔄 Cycle Consistency

* Compares forward vs reversed behavior
* Lower = stable system

#### 🚗 Counting Metrics

* IN count
* OUT count
* Total crossings

---

## 🛠️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/FirstP0P/Object_Detection_and_Tracking.git
cd Object_Detection_and_Tracking
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Download YOLO Model

```python
from ultralytics import YOLO
YOLO("yolov8n.pt")
```

Move to:

```
models/yolov8n.pt
```

---

### 4. Setup SORT

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

1. Click 4 points:

   * Points 1–2 → IN line
   * Points 3–4 → OUT line
2. Press `q` to confirm

---

## 🎥 Video Controls

| Key | Action         |
| --- | -------------- |
| `p` | Pause / Resume |
| `r` | Redraw lines   |
| `q` | Quit           |

---

## 📊 Output

### Visual

* Bounding boxes + IDs
* IN / OUT counters
* Dynamic lines

---

### Saved Results

* Image outputs → `data/output/image/`
* Video outputs → `data/output/video/`
* Metrics (TXT)
* Graphs (PNG)

---

## 🧠 Key Highlights

* ✔ Modular architecture (clean + reusable)
* ✔ Single-pass efficient processing
* ✔ Interactive UI controls
* ✔ Robust counting logic
* ✔ Structured experiment logging

---

## 🏁 Conclusion

This project implements a **complete AI pipeline**:

```
Detection → Tracking → Counting → Evaluation → Logging
```

It demonstrates:

* Real-time system design
* Modular architecture
* Performance evaluation
* Experiment tracking
