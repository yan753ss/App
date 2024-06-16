from datetime import datetime
from app import db

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    request = db.Column(db.String(255), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<LogEntry {self.ip_address} {self.timestamp} {self.request} {self.status_code} {self.size}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
