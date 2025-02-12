from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dataclasses import dataclass
from typing import List
import datetime
from flask_sqlalchemy import SQLAlchemy
import os
import random


app = Flask(__name__)

DATABASE= "app.db"



# Set the database URI
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.secret_key = "your_secret_key"

# Create database and tables
def setup_database():
    with app.app_context():
        db.create_all()

# Database setup
def init_db():
    with sqlite3.connect("app.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                health_status TEXT NOT NULL,
                distance REAL NOT NULL,
                heart_rate INTEGER NOT NULL,
                blood_oxygen INTEGER NOT NULL,
                last_updated TEXT NOT NULL,
                image_url TEXT
            );
        ''')

        conn.commit()

init_db()

if __name__ == '__main__':
    setup_database()

#login
login_manager = LoginManager() #instance of loginmanager class
login_manager.init_app(app) #intializes login manager
login_manager.login_view = 'login' #This attribute specifies the name of the view (or route) that handles the login page.


class User(db.Model, UserMixin):  # Ensure it inherits from db.Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Assuming you have a password field

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return User(id=result[0], username=result[1], email=result[2])
    return None

@app.route("/api/links")
def get_links():
    if current_user.is_authenticated:
        links = [
            {"name": "Home", "url": "/"},
            {"name": "Dashboard", "url": "/dashboard"},
            {"name": "Location", "url": "/location"},
            {"name": "Logout", "url": "/logout"}
        ]
    else:
        links = [
            {"name": "Home", "url": "/"},
            {"name": "Features", "url": "/features"},
            {"name": "Login", "url": "/login"},
            {"name": "Sign Up", "url": "/signup"}
        ]
    
    return jsonify(links)

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    return render_template('home.html')

# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        try:
            with sqlite3.connect("app.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                               (username, email, password))
                conn.commit()
                flash("Account created successfully! Please log in.", "success")
                return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists. Try again.", "danger")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")  # Get the entered password

        # Query the database for the user
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and check_password_hash(user_data[3], password):
            # If the user exists and the password matches
            user = User(id=user_data[0], username=user_data[1], email = user_data[2])
            login_user(user)
            return redirect("/dashboard")
        else:
            flash("Invalid username or password. Please try again.", "error")

    return render_template("login.html")



def get_db():
    """Connect to SQLite database"""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Return results as dictionary-like objects
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection when request is done"""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def get_all_dogs():
    """Fetch all dogs from the database"""
    db = get_db()
    cursor = db.execute("SELECT * FROM dogs")
    return cursor.fetchall()

def get_dog_by_id(dog_id):
    """Fetch a single dog by ID"""
    db = get_db()
    cursor = db.execute("SELECT * FROM dogs WHERE id = ?", (dog_id,))
    return cursor.fetchone()


@app.route("/dog/<int:dog_id>")
def dog_profile(dog_id):
    dog = get_dog_by_id(dog_id)
    if not dog:
        return "Dog not found", 404
    return render_template("dog_profile.html", dog=dog)

# API for real-time pulse data
@app.route("/api/pulse/<int:dog_id>")
def get_pulse(dog_id):
    pulse_data = [random.randint(60, 140) for _ in range(10)]  # Mocked real-time data
    return jsonify(pulse_data)



# Dashboard route (protected)
@app.route("/dashboard")
def dashboard():
    dogs = get_all_dogs()
    return render_template("dashboard.html", dogs=dogs)

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")
@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

