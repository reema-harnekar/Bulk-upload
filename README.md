# Bulk-upload

# Project Name
A bacsic flask query application.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)

## Installation

Follow these instructions to set up your environment and install the necessary dependencies.

### Step 1: Clone the Repository

Clone the repository to your local machine using:

```bash
git clone https://github.com/reema-harnekar/Bulk-upload.git
```

Change to the project directory:

```bash
cd Bulk-upload
```

### Step 2: Create a Virtual Environment

Create a virtual environment:

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

Activate the virtual environment:

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

- **On macOS and Linux:**

  ```bash
  source venv/bin/activate
  ```

### Step 4: Install Required Packages

Install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 5: Set Up PostgreSQL

1. **Install PostgreSQL:**

   - **On Windows:** Download and install from [PostgreSQL official website](https://www.postgresql.org/download/windows/).
   - **On macOS:** Use Homebrew:

     ```bash
     brew install postgresql
     ```

   - **On Linux:** Use your package manager, e.g., for Ubuntu:

     ```bash
     sudo apt-get update
     sudo apt-get install postgresql postgresql-contrib
     ```

2. **Start PostgreSQL Service:**

   - **On Windows:** The service should start automatically; check in the services panel if needed.
   - **On macOS:** Use Homebrew:

     ```bash
     brew services start postgresql
     ```

   - **On Linux:** Start the service using:

     ```bash
     sudo service postgresql start
     ```

3. **Create a Database:**

   Access the PostgreSQL prompt:

   ```bash
   psql postgres
   ```

   Create a new database:

   ```sql
   CREATE DATABASE your_database_name;
   ```

   Exit the PostgreSQL prompt:

   ```sql
   \q
   ```

### Step 6: Set Up Celery

1. **Install Redis (Optional)**: If you're using Redis as a broker for Celery, install it:

   - **On Windows:** Use [Memurai](https://www.memurai.com/) or another method for Windows.
   - **On macOS:** Use Homebrew:

     ```bash
     brew install redis
     ```

   - **On Linux:** Use your package manager, e.g., for Ubuntu:

     ```bash
     sudo apt-get install redis-server
     ```

2. **Start Redis Server** :

   ```bash
   redis-server
   ```

### Step 7: Update Environment Variables

Create a `.env` file in the root directory and add the following environment variables for the application. 

```env
DATABASE_URL="postgresql://username:password@localhost/your_database_name"
SECRET_KEY="replace with secret key"
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "postgresql://username:password@localhost/your_database_name"
```

## Running the Application

1. **Start your application:**

   ```bash
   python3 run.py
   ```

   Replace `app.py` with the name of your main application file.

2. **Start Celery worker (if using Celery):**

   ```bash
   python3 worker.py
   ```

