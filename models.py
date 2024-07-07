from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class tlist(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_time=db.Column(db.DateTime, default=datetime.utcnow)

    
    def __repr__(self):
        return f"tlist {self.sno} - {self.Title}"