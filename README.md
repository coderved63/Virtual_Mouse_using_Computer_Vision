# Hand Gesture-Based Virtual Mouse

A computer vision project that enables touchless mouse control using hand gestures. Built with Python, OpenCV, and MediaPipe.

## Features
- **Touchless Control**: navigate your computer without a physical mouse.
- **Gestures**:
    - **Move Cursor**: Index Finger Up (Thumb must be Down).
    - **Scroll Up**: Index + Middle Fingers Up.
    - **Scroll Down**: Index + Middle + Ring Fingers Up.
    - **Zoom In**: Pinky Finger Up.
    - **Zoom Out**: Pinky + Thumb Up ("Shaka" sign).
    - **Click**: Fist (All fingers down).
    - **Pause/Resume**: Open Palm.
- **Enhanced Precision**: Adaptive smoothing and deadzone implementation for steady control.
- **Real-time Performance**: Optimized utilizing MediaPipe for low-latency tracking.

## System Architecture
- **Hand Detector**: Wraps MediaPipe Hands to detect 21 3D landmarks.
- **Gesture Recognizer**: Boolean logic based on finger states to identify gestures.
- **Mouse Controller**: Maps camera coordinates to screen pixels with Adaptive Smoothing and Deadzone correction using `pyautogui`.

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
- **Move**: Point with Index finger (keep Thumb tucked in).
- **Click**: Make a Fist to click.
- **Scroll**: Use 2 fingers to Scroll Up, 3 fingers to Scroll Down.
- **Zoom**: Hold Pinky Up to Zoom In, hold Pinky+Thumb (Shaka) to Zoom Out.
- **Quit**: Press 'q'.

## Known Limitations
- Extreme lighting conditions can affect detection.
- `pyautogui` fail-safe moves mouse to corner if coordinates go out of bounds (handled via try-except, but be aware).

## Future Improvements
- Deep Learning based custom gesture classification.
- Multi-hand support for complex gestures (e.g., pinch to zoom with two hands).
