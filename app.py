from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dataclasses import dataclass
from typing import List
import random
from datetime import datetime, timedelta
import pytz
import math
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# Email Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "ksmunshi06@gmail.com"
app.config["MAIL_PASSWORD"] = "hvupvlafmctjggqw"
app.config["MAIL_DEFAULT_SENDER"] = "ksmunshi06@gmail.com"

mail = Mail(app)



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
            CREATE TABLE IF NOT EXISTS users (
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
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                heart_rate INTEGER NOT NULL,
                blood_oxygen INTEGER NOT NULL,
                last_updated TEXT NOT NULL,
                image_url TEXT,
                user_id INTEGER REFERENCES users(id)
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

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
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

def send_dog_alert(user_email, dog_name):
    """Send an email alert when a dog's health is in danger."""
    subject = f"🚨 URGENT: {dog_name} Needs Immediate Attention!"
    body = f"Dear User,\n\nYour dog '{dog_name}' is in DANGER! Please check its health metrics immediately.\n\nStay Safe,\nPawsaver"
    
    try:
        msg = Message(subject, recipients=[user_email], body=body)
        mail.send(msg)
        print(f"Alert email sent to {user_email} for {dog_name}")
    except Exception as e:
        print(f"Error sending email: {e}")

def update_dog_status(dog_id, new_status, user_email, dog_name):
    """Update the dog's health status and send an alert if it's in danger."""
    db = get_db()
    db.execute("UPDATE dogs SET health_status = ? WHERE id = ?", (new_status, dog_id))
    db.commit()

    if new_status == "Danger":
        send_dog_alert(user_email, dog_name)  # Send email alert


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

# Function to generate latitude/longitude within a 500m range
def get_nearby_location(user_lat, user_long):
    lat_offset = random.uniform(-0.0045, 0.0045)  # ~500m range
    long_offset = random.uniform(-0.0045, 0.0045)  
    return user_lat + lat_offset, user_long + long_offset

def populate_dogs():
    """Insert sample dog data into the database with realistic, biologically-sound health metrics."""
    db = sqlite3.connect("app.db")
    cursor = db.cursor()

    # Predefined user locations (Replace with actual user locations from DB if stored)
    user_locations = {
        1: (40.7128, -74.0060),  # NYC
        2: (34.0522, -118.2437),  # LA
        3: (51.5074, -0.1278),  # London
    }

    # Health status and corresponding ranges (based on veterinary data)
    # Sources:
    # - Heart Rate:  VCA Animal Hospital, "Heart Rate - General"
    # - Blood Oxygen:  General veterinary knowledge; aim for >95% in healthy dogs
    healthy_range = {
        "heart_rate": (60, 140),  # BPM for resting adult dogs (small breeds tend to be higher)
        "blood_oxygen": (95, 100) # Percentage
    }
    at_risk_range = {
        "heart_rate": (140, 180),  # Slightly elevated heart rate
        "blood_oxygen": (90, 95)  # Mildly reduced oxygen saturation
    }
    danger_range = {
        "heart_rate": (180, 220),  # Significantly elevated; requires immediate attention
        "blood_oxygen": (80, 90)   # Reduced oxygen saturation; concerning
    }

    # Sample dog data
    sample_dogs = [
    ("Sheru", 4, "Healthy", healthy_range, 1),
    ("Golu", 3, "At Risk", at_risk_range, 1),
    ("Mithu", 5, "Healthy", healthy_range, 1),
    ("Kaaluu", 2, "Healthy", healthy_range, 1),
    ("Tinku", 6, "At Risk", at_risk_range, 1),
    ("Bholu", 4, "Healthy", healthy_range, 1),
    ("Chotu", 3, "Healthy", healthy_range, 1),
    ("Jadoo", 5, "At Risk", at_risk_range, 1),
    ("Pari", 2, "Danger", danger_range, 1),
    ("Tommy", 6, "Healthy", healthy_range,1),
    ("Puchkii", 5, "Healthy", healthy_range, 2),
    ("Bittu", 4, "At Risk", at_risk_range, 2),
    ("Oscar", 6, "Healthy", healthy_range, 2),
    ("Sweety", 3, "Healthy", healthy_range, 2),
    ("Olive", 2, "At Risk", at_risk_range, 2),
    ("Ladoo", 4, "Healthy", healthy_range, 2),
    ("Sona", 5, "Healthy", healthy_range, 2),
    ("Pinky", 3, "At Risk", at_risk_range, 2),
    ("Tiger", 6, "Danger", danger_range, 2),
    ("Badal", 4, "Healthy", healthy_range,2),
]

    # Insert data into the dogs table
    for name, age, health_status, ranges, user_id in sample_dogs:
        heart_rate = random.randint(ranges["heart_rate"][0], ranges["heart_rate"][1])
        blood_oxygen = random.randint(ranges["blood_oxygen"][0], ranges["blood_oxygen"][1])

        # Get nearby GPS location based on the user's coordinates
        user_lat, user_long = user_locations[user_id]
        latitude, longitude = get_nearby_location(user_lat, user_long)

        cursor.execute(
            """INSERT INTO dogs (name, age, health_status, latitude, longitude, heart_rate, blood_oxygen, last_updated, image_url, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, age, health_status, latitude, longitude, heart_rate, blood_oxygen, datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S"), "https://goofytails.com/cdn/shop/files/french_bulldog_dog_breed_2000x.jpg?v=1700817521", user_id)
        )

    db.commit()
    db.close()
    print("Sample dogs added successfully!")

# run this function to fill the db
#populate_dogs()

@app.route("/")
def home(): 
    """Redirect authenticated users to the dashboard, otherwise show home page."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))  # Redirect logged-in users to dashboard
    return render_template("home.html")

def classify_health(heart_rate, blood_oxygen):
    """Classify dog's health based on metrics"""
    if heart_rate < 40 or heart_rate > 160 or blood_oxygen < 85:
        return "Danger"
    elif (40 <= heart_rate <= 50) or (150 <= heart_rate <= 160) or (85 <= blood_oxygen <= 90):
        return "At Risk"
    else:
        return "Healthy"

@app.route("/dashboard")
@login_required
def dashboard():
    """Fetch and update all dogs' health status before rendering the dashboard"""
    db = get_db()
    dogs = db.execute("SELECT * FROM dogs WHERE user_id = ?", (current_user.id,)).fetchall()

    for dog in dogs:
        new_status = classify_health(dog["heart_rate"], dog["blood_oxygen"])

        # If status changes, update it and send an alert if "Danger"
       
        update_dog_status(dog["id"], new_status, current_user.email, dog["name"])

    # Fetch updated dogs list for rendering
    dogs = db.execute("SELECT * FROM dogs WHERE user_id = ?", (current_user.id,)).fetchall()
    return render_template("dashboard.html", dogs=dogs)


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


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")
@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


def get_all_dogs():
    """Fetch all dogs belonging to the logged-in user."""
    db = get_db()
    cursor = db.execute("SELECT * FROM dogs WHERE user_id = ?", (current_user.id,))
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

@app.route('/dogs', methods=['GET'])
def get_dogs():
    dogs = [
        {'name': 'Buddy', 'x': 200, 'y': 300},
        {'name': 'Max', 'x': 800, 'y': 400},
        {'name': 'Luna', 'x': 500, 'y': 600}
    ]
    return jsonify(dogs)

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/update_health', methods=['POST'])
def update_health():
    data = request.json
    dog_id = data.get("dog_id")
    heart_rate = data.get("heart_rate")
    blood_oxygen = data.get("blood_oxygen")

    # Store data in SQLite
    db = sqlite3.connect("app.db")
    cursor = db.cursor()
    
    cursor.execute("""
        UPDATE dogs
        SET heart_rate = ?, blood_oxygen = ?, last_updated = ?
        WHERE id = ?
    """, (heart_rate, blood_oxygen, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), dog_id))

    db.commit()
    db.close()

    return jsonify({"message": "Data updated successfully!"})

if __name__ == "__main__":
    app.run(debug=True)

