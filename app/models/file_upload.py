from ..db import db

class FileUpload(db.Model):
    __tablename__ = 'file_uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))