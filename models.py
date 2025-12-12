from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class user(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(256),unique = True, nullable = True, index = True)
    passward_hash = db.Column(db.String(256),nullable = True)
    name = db.Column(db.String(256))
    oauth_provider = db.Column(db.String(50))  # e.g. 'google', 'github', 'facebook'
    oauth_id = db.Column(db.String(256), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<User {self.email}>"
    
    

