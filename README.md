# Bird Detection with YOLOv8 and OpenCV

This project uses the Ultralytics YOLOv8 model and OpenCV to perform real-time bird detection via your webcam. When a bird is detected in the camera feed, the script draws a bounding box around it and saves a snapshot of the frame with a timestamped filename.

---

## Requirements
- Python 3.8+ (not above 3.11)
- [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- OpenCV
- PyTorch (automatically installed with Ultralytics)

### Install dependencies
```bash
pip install ultralytics
```

---

## Usage
1. Make sure your webcam is connected.
2. Download the YOLOv8n model weights (automatically handled on first run).
3. Run the script:
   ```bash
   python main.py
   ```
4. The webcam window will open. When a bird is detected, a snapshot will be saved in the current directory (e.g., `bird_20250420_213308.jpg`).
