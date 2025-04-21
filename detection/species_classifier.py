import cv2
import numpy as np
from PIL import Image

class SpeciesClassifier:
    def __init__(self):
        self.processor = None
        self.model = None
        self.id2label = None

    def _load_model(self):
        if self.model is None or self.processor is None:
            from transformers import EfficientNetImageProcessor, EfficientNetForImageClassification
            self.processor = EfficientNetImageProcessor.from_pretrained("dennisjooo/Birds-Classifier-EfficientNetB2")
            self.model = EfficientNetForImageClassification.from_pretrained("dennisjooo/Birds-Classifier-EfficientNetB2")
            self.id2label = self.model.config.id2label

    def classify(self, image):
        self._load_model()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        inputs = self.processor(image_pil, return_tensors="pt")
        import torch
        with torch.no_grad():
            logits = self.model(**inputs).logits
            predicted_label = logits.argmax(-1).item()
            label = self.id2label.get(predicted_label) or self.id2label.get(str(predicted_label), str(predicted_label))
            prob = torch.nn.functional.softmax(logits, dim=1)[0][predicted_label].item()
        print(f"[DEBUG] Prediction: {label}, prob: {prob}")
        return label, prob