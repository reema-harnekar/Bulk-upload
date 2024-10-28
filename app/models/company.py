from ..db import db

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255))
    year_founded = db.Column(db.Integer)
    industry = db.Column(db.String(255))
    size_range = db.Column(db.String(50))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(255))
    current_employee_estimate = db.Column(db.Integer)
    total_employee_estimate = db.Column(db.Integer)

    # Foreign Key to FileUpload
    file_id = db.Column(db.Integer, db.ForeignKey('file_uploads.id'), nullable=False)
