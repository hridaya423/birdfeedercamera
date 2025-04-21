
from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
import numpy as np
from detection.detector import BirdDetector
from db.logger import DetectionLogger
from utils.notifications import Notifier
from utils.analytics import Analytics
import threading

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, classifier=None):
        super().__init__()
        self.setWindowTitle("Bird Detection System")
        self.setGeometry(100, 100, 1200, 800)
        self.detector = BirdDetector("yolov8n.pt", classifier_model=classifier)
        self.logger = DetectionLogger()
        self.notifier = Notifier()
        self.analytics = Analytics()
        self.init_ui()
        self.capture = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def init_ui(self):
        self.video_label = QtWidgets.QLabel(self)
        self.video_label.setGeometry(10, 10, 800, 600)
        self.stats_btn = QtWidgets.QPushButton("Show Analytics", self)
        self.stats_btn.setGeometry(850, 30, 200, 40)
        self.stats_btn.clicked.connect(self.show_analytics)
        self.export_csv_btn = QtWidgets.QPushButton("Export CSV", self)
        self.export_csv_btn.setGeometry(850, 80, 200, 40)
        self.export_csv_btn.clicked.connect(self.export_csv)
        self.export_pdf_btn = QtWidgets.QPushButton("Export PDF", self)
        self.export_pdf_btn.setGeometry(850, 130, 200, 40)
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        self.log_view = QtWidgets.QTextEdit(self)
        self.log_view.setGeometry(850, 200, 320, 400)
        self.log_view.setReadOnly(True)

    def update_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return
        detections = self.detector.detect(frame)
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            species = det['species']
            conf = det['confidence']
            species_conf = det.get('species_confidence', None)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            label_text = f"{species} ({species_conf:.2f})" if species_conf else f"{species}"
            cv2.putText(frame, f"{label_text} {conf:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            img_path = f"bird_{QtCore.QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')}.jpg"
            cv2.imwrite(img_path, frame)
            self.logger.log_detection(species, conf, img_path)
            self.notifier.send_desktop_notification("Bird Detected", f"{species} ({conf:.2f})")
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), QtCore.Qt.KeepAspectRatio))
        self.update_log_view()

    def update_log_view(self):
        logs = self.logger.get_detections()
        self.log_view.clear()
        for log in logs[-10:]:
            # log[2]=species, log[3]=confidence
            self.log_view.append(f"{log[1]} - {log[2]} ({log[3]:.2f})")

    def show_analytics(self):
        threading.Thread(target=self.analytics.plot_species_pie).start()

    def export_csv(self):
        self.analytics.export_csv("detections.csv")

    def export_pdf(self):
        self.analytics.export_pdf("detections.pdf")
