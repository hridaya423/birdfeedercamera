
import matplotlib.pyplot as plt
import sqlite3
import csv
from reportlab.pdfgen import canvas
from datetime import datetime

class Analytics:
    def __init__(self, db_path="detections.db"):
        self.conn = sqlite3.connect(db_path)

    def most_common_species(self, top_n=5):
        cur = self.conn.cursor()
        cur.execute('SELECT species, COUNT(*) as cnt FROM detections GROUP BY species ORDER BY cnt DESC LIMIT ?', (top_n,))
        return cur.fetchall()

    def detection_trends(self):
        cur = self.conn.cursor()
        cur.execute('SELECT substr(timestamp, 1, 10) as date, COUNT(*) FROM detections GROUP BY date ORDER BY date')
        return cur.fetchall()

    def export_csv(self, out_path):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM detections')
        rows = cur.fetchall()
        with open(out_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'timestamp', 'species', 'confidence', 'image_path'])
            writer.writerows(rows)

    def export_pdf(self, out_path):
        c = canvas.Canvas(out_path)
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM detections')
        rows = cur.fetchall()
        c.drawString(100, 800, 'Bird Detection Report')
        y = 780
        for row in rows:
            c.drawString(50, y, str(row))
            y -= 20
            if y < 50:
                c.showPage()
                y = 800
        c.save()

    def plot_species_pie(self):
        data = self.most_common_species()
        labels = [d[0] for d in data]
        sizes = [d[1] for d in data]
        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Most Common Bird Species')
        plt.show()
