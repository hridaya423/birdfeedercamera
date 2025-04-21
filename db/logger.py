import sqlite3
from datetime import datetime

class DetectionLogger:
    def __init__(self, db_path="detections.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    species TEXT,
                    confidence REAL,
                    image_path TEXT
                )
            ''')

    def log_detection(self, species, confidence, image_path):
        with self.conn:
            self.conn.execute('''
                INSERT INTO detections (timestamp, species, confidence, image_path)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), species, confidence, image_path))

    def get_detections(self, species=None, start=None, end=None):
        query = 'SELECT * FROM detections WHERE 1=1'
        params = []
        if species:
            query += ' AND species=?'
            params.append(species)
        if start:
            query += ' AND timestamp>=?'
            params.append(start)
        if end:
            query += ' AND timestamp<=?'
            params.append(end)
        return self.conn.execute(query, params).fetchall()
