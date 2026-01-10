# Hand Gesture-Based Virtual Mouse

A computer vision project that enables touchless mouse control using hand gestures. Built with Python, OpenCV, and MediaPipe.

## Features
- **Touchless Control**: navigate your computer without a physical mouse.
- **Gestures**:
    - **Index Finger**: Move Cursor
    - **Index + Middle Finger**: Scroll
    - **Thumb + Index Pinch**: Zoom (or visual feedback)
    - **Fist**: Click
    - **Open Palm**: Pause/Resume
- **Real-time Performance**: Optimized utilizing MediaPipe for low-latency tracking.

## System Architecture
- **Hand Detector**: Wraps MediaPipe Hands to detect 21 3D landmarks.
- **Gesture Recognizer**: Boolean logic based on finger states and euclidian distances.
- **Mouse Controller**: Maps camera coordinates to screen pixels with Exponential Moving Average (EMA) smoothing using `pyautogui`.

## Installation

### Prerequisites
- Python 3.9+
- Webcam

### Setup Instructions

1. **Create and Activate Virtual Environment**:

   **Windows:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python src/main.py
   ```

## Usage
- Ensure good lighting.
- Keep your hand within 1-2 meters of the webcam.
- **Move**: Point with Index finger.
- **Click**: Make a Fist.
- **Scroll**: Raise Index and Middle fingers.
- **Quit**: Press 'q'.

## Known Limitations
- Extreme lighting conditions can affect detection.
- `pyautogui` fail-safe moves mouse to corner if coordinates go out of bounds (handled via try-except, but be aware).

## Future Improvements
- Deep Learning based custom gesture classification.
- Multi-hand support for complex gestures (e.g., pinch to zoom with two hands).
