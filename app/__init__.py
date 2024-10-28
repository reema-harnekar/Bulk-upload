from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .db import db
from .models import User
from .models import FileUpload
from .models import Company
from config import Config
from celery import Celery
import os
import datetime
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)

celery_instance = Celery(app.name,
                         broker=app.config['CELERY_RESULT_BACKEND'],
                         backend=app.config['CELERY_BROKER_URL']
                         )

celery_instance.conf.update(app.config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect unauthenticated users to the login page

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/total_records', methods=['GET'])
def total_records():
    count = db.session.query(Company).count()  # Assuming Company is your model
    return jsonify({'total': count})

@app.route('/api/industries', methods=['GET'])
def industries():
    unique_industries = db.session.query(Company.industry).distinct().all()
    return jsonify([industry[0] for industry in unique_industries])

@app.route('/api/years_founded', methods=['GET'])
def years_founded():
    unique_years = db.session.query(Company.year_founded).distinct().all()
    return jsonify([year[0] for year in unique_years])

@app.route('/api/cities', methods=['GET'])
def cities():
    unique_cities = db.session.query(Company.city).distinct().all()
    return jsonify([city[0] for city in unique_cities])

@app.route('/api/states', methods=['GET'])
def states():
    unique_states = db.session.query(Company.state).distinct().all()
    return jsonify([state[0] for state in unique_states])

@app.route('/api/countries', methods=['GET'])
def countries():
    unique_countries = db.session.query(Company.country).distinct().all()
    return jsonify([country[0] for country in unique_countries])

@app.route('/submit_query', methods=['POST'])
def submit_query():
    keyword = request.form.get('keyword', '')
    industry = request.form.get('industry', '')
    year_founded = request.form.get('year_founded', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    country = request.form.get('country', '')
    
    query = db.session.query(Company)

    if keyword:
        query = query.filter(Company.name.ilike(f"%{keyword}%"))
    if industry:
        query = query.filter(Company.industry == industry)
    if year_founded:
        query = query.filter(Company.year_founded == year_founded)
    if city:
        query = query.filter(Company.city == city)
    if state:
        query = query.filter(Company.state == state)
    if country:
        query = query.filter(Company.country == country)

    total_records = query.count()
    
    return jsonify({'total_records': total_records})

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('upload_data'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

# Route to render the file upload page
@app.route('/upload_data', methods=['GET'])
@login_required  # Ensure only logged-in users can access this route
def upload_data():
    return render_template('upload_data.html')

@app.route('/upload_file', methods=['POST'])
@login_required  # Ensure only logged-in users can access this route
def upload_file():
    file = request.files.get('file')
    if file and file.filename.endswith('.csv'):
        # Save the file to the desired location
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        uploaded_at = datetime.datetime.now()
        file.save(file_path)

        # Insert file data into the database (assuming a FileUpload model exists)
        new_file = FileUpload(filename=filename, filepath=file_path, user_id=current_user.id, uploaded_at=uploaded_at)
        db.session.add(new_file)
        db.session.commit()

        process_csv.delay(file_path, new_file.id)

        return jsonify({'message': 'File uploaded successfully!'}), 200
    else:
        return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

@app.route('/query_builder', methods=['GET', 'POST'])
def query_builder():
    return render_template('query_builder.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@celery_instance.task(name="process_csv")
def process_csv(file_path, file_id):
    try:
        with app.app_context():
            # Process CSV in chunks
            chunk_size = 10000
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                # Process each row in the chunk
                for index, row in chunk.iterrows():
                    # Split 'locality' into city, state, country
                    locality = row['locality'].split(',') if pd.notnull(row['locality']) else ["", "", ""]
                    city = locality[0] if len(locality) > 0 else None
                    state = locality[1] if len(locality) > 1 else None
                    country = locality[2] if len(locality) > 2 else row.get('country', None)

                    # Create Company instance and link it to the file_id
                    company = Company(
                        name=row['name'],
                        domain=row['domain'],
                        year_founded=int(row['year founded']) if pd.notnull(row['year founded']) else None,
                        industry=row['industry'],
                        size_range=row['size range'],
                        city=city,
                        state=state,
                        country=country,
                        linkedin_url=row['linkedin url'],
                        current_employee_estimate=int(row['current employee estimate']) if pd.notnull(row['current employee estimate']) else None,
                        total_employee_estimate=int(row['total employee estimate']) if pd.notnull(row['total employee estimate']) else None,
                        file_id=file_id  # Associate with FileUpload
                    )
                    db.session.add(company)

                # Commit each chunk
                db.session.commit()

            return {'status': 'success'}
    except Exception as e:
        db.session.rollback()
        return {'status': 'failure', 'error': str(e)}
    

def create_default_user():
    # Check if the user already exists
    existing_user = User.query.filter_by(username="User1").first()
    if not existing_user:
        default_user = User(username="User1", email="user1@example.com")
        default_user.set_password("12345678")  # Set the default password
        db.session.add(default_user)
        db.session.commit()
        print("Default user created: User1")

with app.app_context():
    db.create_all()
    create_default_user()

if __name__ == '__main__':
    app.run(debug=True)