from datetime import datetime
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True, default='default.jpg')  # Add this line
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
