from ultralytics import YOLO
import cv2
from datetime import datetime

model = YOLO("yolov8n.pt") 

cap = cv2.VideoCapture(0)

print("[INFO] Starting YOLOv8 bird detection...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    bird_detected = False

    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls_id]

        if label == "bird" and conf > 0.4:
            bird_detected = True
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bird_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"[INFO] Bird detected! Saved: {filename}")
            break

    cv2.imshow("YOLOv8 Bird Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
