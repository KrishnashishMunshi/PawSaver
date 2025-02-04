from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dataclasses import dataclass
from typing import List
import datetime
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)


@dataclass
class DogHealth:
    id: int
    name: str
    heart_rate: int
    blood_oxygen: float
    health_status: str
    last_updated: datetime.datetime

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

class DogHealthMonitor:
    def __init__(self):
        # Sample static data
        self.dogs = [
            DogHealth(1, "Max", 75, 98.5, "Healthy", datetime.datetime.now()),
            DogHealth(2, "Luna", 82, 97.2, "Active", datetime.datetime.now()),
            DogHealth(3, "Rocky", 90, 96.8, "Needs Rest", datetime.datetime.now())
        ]
    
    def get_all_dogs(self) -> List[DogHealth]:
        return self.dogs
    
    def get_dog_by_id(self, dog_id: int) -> DogHealth:
        return next((dog for dog in self.dogs if dog.id == dog_id), None)

monitor = DogHealthMonitor()

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

# Dashboard route (protected)
@app.route("/dashboard")
def dashboard():
    
    return render_template("dashboard.html",   dogs=monitor.get_all_dogs())

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
