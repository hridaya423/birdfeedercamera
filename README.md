# Bird Detection and Species Classification with YOLOv8, OpenCV, and Hugging Face

This project uses the Ultralytics YOLOv8 model and OpenCV for real-time bird detection via your webcam. When a bird is detected in the camera feed, the script draws a bounding box around it and saves a snapshot of the frame with a timestamped filename. Additionally, the detected bird is classified to species level using a EfficientNet-B2 model from Hugging Face.

---

## Requirements
- Python 3.8+ (not above 3.11)
- [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- OpenCV
- PyTorch (automatically installed with Ultralytics)
- torchvision
- transformers

### Install dependencies
```bash
pip install requirements.txt
```

---

## Usage
1. Make sure your webcam is connected.
2. Run the script:
   ```bash
   python main.py
   ```
3. The webcam window will open. When a bird is detected, a snapshot will be saved in the current directory (e.g., `bird_20250420_213308.jpg`).
4. The detected bird will be classified in real-time, and the species name and confidence will be displayed in the debug output.

---

## Model Details
- **Object Detection**: YOLOv8 (Ultralytics)
- **Bird Species Classification**: [dennisjooo/Birds-Classifier-EfficientNetB2](https://huggingface.co/dennisjooo/Birds-Classifier-EfficientNetB2) via Hugging Face Transformers

