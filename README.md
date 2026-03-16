<div align="center">

# 🧠 NeuroLearn Gesture Navigator

### *Explore Reinforcement Learning with Your Hands*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-ML_Model-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand_Tracking-00897B?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev/)
[![OpenGL](https://img.shields.io/badge/PyOpenGL-3D_Rendering-5586A4?style=for-the-badge&logo=opengl&logoColor=white)](https://pyopengl.sourceforge.net/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

> **NeuroLearn Gesture Navigator** is a touchless, immersive educational interface that lets you explore complex Reinforcement Learning concepts by navigating a **living 3D neural network graph** — controlled entirely by your hand gestures through a standard webcam.

<br/>

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🤚 Gesture Controls](#-gesture-controls)
- [🛠️ Technology Stack](#️-technology-stack)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [⚙️ Configuration](#️-configuration)
- [🏗️ Project Architecture](#️-project-architecture)
- [📂 Project Structure](#-project-structure)
- [🤖 Training the Gesture Model](#-training-the-gesture-model)
- [🔧 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

NeuroLearn features a custom-built **3D OpenGL rendering engine** designed to mimic living biological tissue, transforming abstract RL knowledge into a tangible, explorable "brain" of information.

| Feature | Description |
|---|---|
| 🧿 **Living Wobbly Dendrites** | Knowledge-node connections are organic, Bézier-curved strings that breathe and wobble in real time. |
| 💫 **3D Triple-Layered Nodes** | Each neuron is rendered with a bright-white inner core, a glowing blue shell, and a pulsating semi-transparent outer membrane. |
| 💥 **Interactive Node Repulsion** | The neural network physically reacts to your hand — nodes spring and repel away from your cursor as it moves through 3D space. |
| ☄️ **Synaptic Explosions & Pulses** | Hovering over a node triggers a 3D burst of neurotransmitter particles; synaptic signals randomly fire across dendritic connections. |
| 🎥 **Cinematic Rotational Inertia** | Spin the brain graph and watch it glide to a smooth stop — the graph carries realistic rotational momentum. |
| 🌁 **Volumetric Fog & Depth of Field** | Distant and unfocused nodes fade naturally into deep volumetric fog, enhancing the parallax 3D effect. |
| 📚 **50+ RL Concept Nodes** | A curated, interconnected curriculum covering everything from MDPs and Bellman equations to DQN, PPO, and SAC. |

---

## 🤚 Gesture Controls

The application uses a **custom PyTorch Neural Network** trained on 42-dimensional hand-landmark features from MediaPipe to classify gestures in real time.

<br/>

<div align="center">

| Gesture | Action | Description |
|:---:|:---:|---|
| ☝️ **Point** | Hover & Explore | Extend your index finger to guide the bioluminescent cursor. Hovering over a node reveals its RL concept details. |
| 🤏 **Pinch** | Zoom | Pinch index finger and thumb together and move your hand toward/away from the camera to zoom the viewport. |
| ✋ **Open Hand** | Rotate | Spread your hand open and move it to spin the entire 3D neural network. Release to glide with cinematic momentum. |
| ✊ **Closed Fist** | Cancel / Close | Close your fist to dismiss any open info panels. |
| 👉 **Swipe Left / Right** | Navigate | Swipe left or right for panel navigation actions. |

</div>

<br/>

> 💡 **Two-Hand Zoom:** Place both hands in frame and spread/pinch them apart for smoother, more intuitive zoom control.

---

## 🛠️ Technology Stack

<div align="center">

| Layer | Technology | Purpose |
|---|---|---|
| **Computer Vision** | MediaPipe, OpenCV | Hand landmark detection & webcam processing |
| **Machine Learning** | PyTorch, Scikit-learn | Custom 6-class gesture classifier (42-feature MLP) |
| **3D Rendering** | PyOpenGL, Pygame | High-performance 3D scene rendering & window management |
| **Graph & Math** | NetworkX, NumPy | 3D spring-force graph layout & linear algebra |
| **Configuration** | python-dotenv | Environment-based runtime configuration |
| **Visualization** | Matplotlib | Data inspection and model diagnostics |

</div>

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- A working **webcam** (built-in or USB)
- A system capable of running OpenGL (most modern PCs/Macs)

### Installation

**1. Clone the repository:**

```bash
git clone https://github.com/darknecrocities/neurolearn-RL-agent.git
cd neurolearn-RL-agent
```

**2. Create and activate a virtual environment** *(recommended)*:

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies:**

> ⚠️ Use the pinned versions in `requirements.txt` to ensure compatibility, especially for MediaPipe on Windows.

```bash
pip install -r requirements.txt
```

### Running the Application

Ensure your webcam is **not** in use by another application, then:

```bash
python app/main.py
```

The 3D neural network will launch in a `1024×768` window. Position your hand in the webcam's view and start exploring!

> Press **`ESC`** or close the window to exit.

---

## ⚙️ Configuration

NeuroLearn is configured via a `.env` file in the project root. Create one by copying the example below:

```ini
# .env — NeuroLearn Configuration

# Index of the webcam device to use (default: 0 for the primary camera)
CAMERA_INDEX=0

# Path to the trained PyTorch gesture classifier weights
GESTURE_MODEL_PATH=models/gesture_model.pth

# Path to the RL curriculum JSON file
LESSON_DATA=data/rl_lessons.json

# Cursor smoothing factor (0.0 = raw, 1.0 = maximum smoothing)
CURSOR_SMOOTHING=0.75

# Distance threshold (normalized) for detecting a manual pinch gesture
PINCH_THRESHOLD=0.04

# Multiplier for 3D graph rotation speed
GRAPH_ROTATION_SPEED=0.6
```

All variables are optional — sensible defaults are applied if a `.env` file is absent.

---

## ��️ Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Webcam Feed                          │
└──────────────────────────┬──────────────────────────────────┘
                           │ Raw Frame (BGR)
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    Vision Layer                              │
│   HandTracker (MediaPipe)  →  LandmarkProcessor (Normalize) │
└──────────────────────────┬───────────────────────────────────┘
                           │ 42-Feature Vector
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                  Machine Learning Layer                      │
│   GestureClassifier (PyTorch MLP 42→128→64→32→6 classes)    │
└──────┬──────────────────┬──────────────────┬─────────────────┘
       │ Class 0 (Hover)  │ Class 1 (Pinch)  │ Class 2/3 (Rotate/Cancel)
       ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────────────┐
│               Application Control Layer                      │
│   CursorController  │  CameraRotation (Zoom/Inertia)        │
│   LessonManager     │  NeuronGraph (Node Repulsion Physics)  │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                   Rendering Layer                            │
│   PyOpenGL (3D Scene)  +  Pygame Surface (2D HUD Overlay)   │
│   GraphRenderer → Nodes, Dendrites, Particles, Fog          │
│   InfoPanel → RL Concept Panel on Hover                     │
└──────────────────────────────────────────────────────────────┘
```

---

## �� Project Structure

```
neurolearn-RL-agent/
│
├── app/                          # Application logic & control layer
│   ├── main.py                   # Entry point, game loop & OpenGL setup
│   ├── cursor_controller.py      # Maps hand position → smoothed 2D screen cursor
│   ├── gesture_controller.py     # Loads PyTorch model & predicts gesture class
│   └── lesson_manager.py         # Manages info panel open/close state
│
├── vision/                       # Computer vision pipeline
│   ├── hand_tracker.py           # MediaPipe Hands wrapper
│   └── landmark_processor.py     # Landmark normalization → 42-feature vector
│
├── visualization/                # PyOpenGL 3D rendering engine
│   ├── graph_renderer.py         # Renders nodes, Bézier dendrites & particles
│   ├── neuron_graph.py           # NetworkX spring-layout graph + repulsion physics
│   ├── camera_rotation.py        # 3D rotation math, zoom & inertia
│   └── info_panel.py             # 2D HUD overlay for RL concept descriptions
│
├── models/                       # ML model definition & training
│   ├── gesture_classifier.py     # PyTorch MLP model definition (42 → 6 classes)
│   ├── gesture_model.pth         # Pre-trained gesture classifier weights
│   └── train_gesture_model.py    # Script to retrain the gesture model
│
├── data/
│   └── rl_lessons.json           # Curriculum: 50+ RL concept nodes & connections
│
├── utils/
│   ├── math_utils.py             # Helper: Euclidean distance calculation
│   └── smoothing.py              # Helper: Exponential moving average smoothing
│
├── requirements.txt              # Pinned Python dependencies
└── .env                          # (Optional) Runtime configuration overrides
```

---

## 🤖 Training the Gesture Model

A pre-trained model (`models/gesture_model.pth`) is included and ready to use. If you wish to **retrain** it (e.g., to improve accuracy with your own gesture data), run:

```bash
python models/train_gesture_model.py
```

This trains a 6-class MLP on synthetic landmark data and saves updated weights to `models/gesture_model.pth`.

**Gesture Class Mapping:**

| Class | Label | Triggered Action |
|:---:|---|---|
| `0` | `move_cursor` | Hover & explore nodes |
| `1` | `pinch_select` | Zoom in/out |
| `2` | `open_hand_rotate` | Rotate the 3D graph |
| `3` | `closed_fist_cancel` | Close info panel |
| `4` | `swipe_left` | Navigate left |
| `5` | `swipe_right` | Navigate right |

---

## 🔧 Troubleshooting

<details>
<summary><strong>❌ Camera not opening / "Could not open camera 0"</strong></summary>

- Ensure no other application (e.g., Zoom, Teams) is using the webcam.
- Try a different camera index by setting `CAMERA_INDEX=1` in your `.env` file.
- On Linux, verify you have read access to `/dev/video0`.

</details>

<details>
<summary><strong>❌ Gesture model not found warning</strong></summary>

- Run `python models/train_gesture_model.py` from the project root to generate `models/gesture_model.pth`.
- Verify `GESTURE_MODEL_PATH` in your `.env` points to the correct file path.

</details>

<details>
<summary><strong>❌ MediaPipe / OpenCV compatibility error on Windows</strong></summary>

- Ensure you are using the exact pinned version: `mediapipe==0.10.14`
- Use Python **3.11** — MediaPipe may not support newer versions on Windows.
- Install via: `pip install mediapipe==0.10.14`

</details>

<details>
<summary><strong>❌ OpenGL / Pygame window fails to open</strong></summary>

- Ensure your graphics drivers are up to date.
- On headless servers, OpenGL requires a virtual display (e.g., `Xvfb`).
- macOS users may need to set `PYGAME_DISPLAY=0` and run from a native terminal.

</details>

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** this repository
2. Create a **feature branch**: `git checkout -b feature/my-new-feature`
3. **Commit** your changes: `git commit -m 'Add some feature'`
4. **Push** to the branch: `git push origin feature/my-new-feature`
5. Open a **Pull Request**

Please ensure your code follows the existing style and that any new gestures or nodes are reflected in both the code and `data/rl_lessons.json`.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

*Designed and developed as an interactive exploration of machine learning principles.*

**[⬆ Back to top](#-neurolearn-gesture-navigator)**

</div>
