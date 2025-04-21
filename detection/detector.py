import cv2
from ultralytics import YOLO
import numpy as np
from detection.species_classifier import SpeciesClassifier

class BirdDetector:
    def __init__(self, yolo_model_path, classifier_model=None):
        self.model = YOLO(yolo_model_path)
        self.classifier = classifier_model or SpeciesClassifier()

    def detect(self, frame):
        results = self.model(frame)[0]
        detections = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = self.model.names[cls_id]
            if label == "bird" and conf > 0.4:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                species = None
                species_conf = None
                if self.classifier:
                    crop = frame[y1:y2, x1:x2]
                    if crop.size > 0:
                        species, species_conf = self.classify_species(crop)
                detections.append({
                    'bbox': (x1, y1, x2, y2),
                    'confidence': conf,
                    'species': species or 'bird',
                    'species_confidence': species_conf
                })
        return detections

    def classify_species(self, image):
        return self.classifier.classify(image)
