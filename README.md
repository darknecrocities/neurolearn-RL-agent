# NeuroLearn Gesture Navigator

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![OpenGL](https://img.shields.io/badge/OpenGL-PyOpenGL-5586A4?style=for-the-badge&logo=opengl)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Google-00569E?style=for-the-badge&logo=google)
![PyTorch](https://img.shields.io/badge/PyTorch-ML_Model-EE4C2C?style=for-the-badge&logo=pytorch)

**NeuroLearn Gesture Navigator** is a cutting-edge, touchless educational interface. It allows users to explore complex Reinforcement Learning (RL) concepts by navigating a 3D, living neural network graph using only hand gestures captured via a standard webcam.

By combining computer vision, machine learning gesture classification, and high-performance 3D rendering, this project turns abstract knowledge into a tangible, explorable "brain" of information.

---

## Features (V4 Hyper-Realism)

This project features a custom-built 3D OpenGL rendering engine designed to mimic living biological tissue:

- **\ud83e\uddbf Living Wobbly Dendrites:** Connections between knowledge nodes are not rigid lines, but organic, Bezier-curved strings that slowly breathe and wobble over time.
- **\ud83d\udcab 3D Triple-Layered Nodes:** Each neuron is rendered with immense depth, featuring a dense bright-white inner core, a glowing blue shell, and a pulsating semi-transparent outer membrane.
- **\ud83d\udca5 Interactive Node Repulsion:** As your hand moves through the 3D space, the neural network reacts physically, with nodes springing and repelling away from your cursor.
- **\u2604\ufe0f Synaptic Explosions & Pulses:** Hovering over a new node triggers a 3D burst of neurotransmitter particles. Glowing synaptic signals randomly fire across the dendritic connections.
- **\ud83c\udfa5 Cinematic Rotational Inertia:** Grabbing and spinning the brain graph feels heavy and premium. The graph carries rotational momentum, allowing you to swipe and watch it glide to a smooth stop.
- **\ud83c\udf01 Volumetric Fog & Depth of Field:** Unfocused and distant nodes naturally fade into deep volumetric fog, enhancing the parallax 3D effect.

---

## Gesture Controls

The application uses a custom PyTorch Neural Network and MediaPipe to classify your hand gestures in real-time:

*   **\ud83d\udc46 Hover & Explore (Point):** Use your index finger to guide the bioluminescent on-screen cursor. Hovering over a node will instantly reveal its detailed Reinforcement Learning information.
*   **\u270a Rotate (Fist/Grab):** Trigger the rotation gesture and move your hand to spin the entire 3D neural network. Release to let it glide with cinematic momentum.
*   **\ud83e\udd0f Zoom (Pinch):** Pinch your index finger and thumb together. Moving your hand closer to or further from the camera will seamlessly zoom the 3D viewport in and out.
*   **\ud83d\udd50 Cancel/Close (Open Hand):** Use the cancel gesture to close out of any focused views.

---

## Technology Stack

*   **Computer Vision:** `MediaPipe` (Hand Landmarks), `OpenCV` (Webcam processing)
*   **Machine Learning:** `PyTorch` (Custom Gesture Classifier), `Scikit-learn` (Preprocessing)
*   **3D Rendering:** `PyOpenGL`, `Pygame` (Window & Event Management)
*   **Mathematics & Graphing:** `NumPy`, `NetworkX` (3D Spring Layouts)

---

## Getting Started

### Prerequisites

*   Python 3.11+
*   A working webcam

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/neurolearn-gesture-navigator.git
    cd neurolearn-gesture-navigator
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Make sure to use the specific pinned versions in `requirements.txt` to ensure compatibility (especially for MediaPipe on Windows).
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Ensure your webcam is not being used by another application, then run:

```bash
python app/main.py
```

---

## Project Structure

```text
neurolearn-gesture-navigator/
\u251c\u2500\u2500 app/                    # Main application logic
\u2502   \u251c\u2500\u2500 main.py             # Entry point & game loop
\u2502   \u251c\u2500\u2500 cursor_controller.py# 2D Screen cursor mapping
\u2502   \u251c\u2500\u2500 gesture_controller.py# ML Gesture Prediction
\u2502   \u2514\u2500\u2500 lesson_manager.py   # UI panel state management
\u251c\u2500\u2500 data/                   # Content & Models
\u2502   \u251c\u2500\u2500 rl_lessons.json     # Node curriculum data
\u2502   \u2514\u2500\u2500 gesture_model.pth   # PyTorch classifier weights
\u251c\u2500\u2500 vision/                 # Computer Vision modules
\u2502   \u251c\u2500\u2500 hand_tracker.py     # MediaPipe wrapper
\u2502   \u2514\u2500\u2500 landmark_processor.py# Landmark normalization
\u251c\u2500\u2500 visualization/          # PyOpenGL Rendering Engine
\u2502   \u251c\u2500\u2500 camera_rotation.py  # 3D Math & Inertia
\u2502   \u251c\u2500\u2500 graph_renderer.py   # Node, Edge, Particle rendering
\u2502   \u251c\u2500\u2500 info_panel.py       # HUD overlay
\u2502   \u2514\u2500\u2500 neuron_graph.py     # NetworkX Spring Physics
\u2514\u2500\u2500 requirements.txt        # Pinned dependencies
```

---

*Designed and developed as an interactive exploration of machine learning principles.*
