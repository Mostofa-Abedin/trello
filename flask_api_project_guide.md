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

## Step 7: Adding Blueprints and CLI Commands

1. **Create Controllers Folder and CLI Commands**

```python
from flask import Blueprint
from init import db
from models.user import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped!")

@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(email="admin@test.com", password=bcrypt.generate_password_hash("123456").decode('utf-8'), is_admin=True),
        User(email="user@test.com", password=bcrypt.generate_password_hash("123456").decode('utf-8'), is_admin=False)
    ]
    db.session.add_all(users)
    db.session.commit()
    print("Tables seeded!")
```

2. **Register Blueprints in main.py**

Add this to your main.py file to register the blueprint:

```python
from controllers.cli_controllers import db_commands

app = Flask(__name__)
# Blueprint registration
app.register_blueprint(db_commands)
```

3. **Run CLI Commands**
   After registering the blueprints, you can now run the following CLI commands in your terminal:

```bash
flask db create   # Creates all tables
flask db drop     # Drops all tables
flask db seed     # Seeds the tables with initial data
```

### Step 8: User Model and Authentication

1. **Create User Model**

In your models folder, create a user.py file with the following content:

```python
from init import db, ma

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
```

2. **Authentication Routes**

In your controllers folder, create a new file called auth_controller.py and add the following routes for user registration and login:

```python
from flask import Blueprint, request
from init import db, bcrypt
from models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(
        email=data['email'],
        password=bcrypt.generate_password_hash(data['password']).decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()
    return {'message': 'User registered successfully!'}
```
