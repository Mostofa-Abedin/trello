
# Step-by-Step Guide for Setting up an API Project with Flask

## Step 1: Project Setup

1. **Create Project Directory**: 
   - Create a new folder for your project (e.g., `trello_clone`).
   
2. **Create Virtual Environment**:
   - Open your terminal and navigate to the project folder.
   - Run the command to create a virtual environment:
     ```bash
     python3 -m venv .venv
     ```
   - Activate the virtual environment:
     - On MacOS/Linux:
       ```bash
       source .venv/bin/activate
       ```
     - On Windows:
       ```bash
       .venv\Scripts\activate
       ```

## Step 2: Install Necessary Packages

1. Install the following Flask-related libraries:
   ```bash
   pip install Flask SQLAlchemy flask-marshmallow Flask-Bcrypt Flask-JWT-Extended python-dotenv psycopg2-binary
   ```

2. **Create `requirements.txt`**:
   - After installing the packages, create a `requirements.txt` file to track dependencies:
     ```bash
     pip freeze > requirements.txt
     ```

## Step 3: Create Configuration Files

1. **`.env` File**: 
   - Create a `.env` file for sensitive information like the database URL and JWT secret key:
     ```bash
     DATABASE_URL = "postgresql+psycopg2://trello_dev:123456@localhost:5432/trello_db"
     JWT_SECRET_KEY = "secret"
     ```

2. **`.env.example`**: 
   - Create an example `.env` file without sensitive data, which other users can use to set up their environment:
     ```bash
     DATABASE_URL = 
     JWT_SECRET_KEY = 
     ```

3. **`.flaskenv` File**:
   - Create a `.flaskenv` file to configure the Flask app:
     ```bash
     FLASK_APP=main
     FLASK_DEBUG=1
     FLASK_RUN_PORT=8080
     ```

4. **`.gitignore` File**:
   - Create a `.gitignore` file to exclude unnecessary or sensitive files:
     ```bash
     __pycache__
     .venv
     .env
     ```

## Step 4: Initialize the App

1. **Create `init.py`**: 
   - Create a file called `init.py` to initialize the libraries needed for the app:
     ```python
     from flask_sqlalchemy import SQLAlchemy
     from flask_marshmallow import Marshmallow
     from flask_bcrypt import Bcrypt
     from flask_jwt_extended import JWTManager

     db = SQLAlchemy()
     ma = Marshmallow()
     bcrypt = Bcrypt()
     jwt = JWTManager()
     ```

2. **Create `main.py`**:
   - Create a `main.py` file to set up the Flask app and link it to the database and JWT:
     ```python
     import os
     from flask import Flask
     from init import db, ma, bcrypt, jwt

     def create_app():
         app = Flask(__name__)
         app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
         app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET_KEY")

         db.init_app(app)
         ma.init_app(app)
         bcrypt.init_app(app)
         jwt.init_app(app)

         return app
     ```

## Step 5: Set Up the Database

1. **PostgreSQL Setup**:
   - Create a PostgreSQL database for the project.
     ```bash
     sudo -u postgres psql
     ```
   - Inside the PostgreSQL console, run the following commands:
     ```sql
     CREATE DATABASE trello_db;
     CREATE USER trello_dev WITH PASSWORD '123456';
     GRANT ALL PRIVILEGES ON DATABASE trello_db TO trello_dev;
     ```

## Step 6: Run the App

1. **Run the Flask App**:
   - After setting everything up, run the app using the following command:
     ```bash
     flask run
     ```

This is the initial setup for building an API from scratch, including environment configurations, database setup, and project structure. We’ll expand this guide with more models, views, and controllers as we progress through the lectures.
