from sqlite3 import IntegrityError
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from jumping import run_jumping_jack_app, stop_execution_internal, show_congratulations, get_username
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password = db.Column(db.String(60), nullable=False)

# Load a user by ID for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Default route is the registration page
@app.route('/')
def homepage():
    return render_template('MainFitQuest.html')

# Default route is the home page
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# Default route is the activities page
@app.route('/activities', methods=['GET', 'POST'])
def activities():
    return render_template('activities.html')

# Default route is the nav page
@app.route('/nav', methods=['GET', 'POST'])
def nav():
    return render_template('nav.html')

# Default route is the leaderboard page
@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/get_user_info')
def get_user_info():
    # Read the contents of the user_info.txt file
    file_path = os.path.join(app.root_path, 'user_info.txt')
    with open(file_path, 'r') as file:
        user_info = file.readlines()

    # Parse the user_info and create a list of dictionaries
    leaderboard = []
    for line in user_info:
        parts = line.strip().split(', ')
        username = parts[0].split(': ')[1]
        count = int(parts[1].split(': ')[1])
        leaderboard.append({'name': username, 'number': count})

    # Sort the leaderboard in descending order based on the 'number' property
    leaderboard.sort(key=lambda x: x['number'], reverse=True)

    return jsonify(leaderboard)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            user = User(id=username, username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists. Please choose a different one.', 'danger')

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            # User exists, check password
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Login failed. Incorrect password. Please try again.', 'danger')
        else:
            flash('Login failed. Username not found. Please check your username.', 'danger')

    return render_template('login.html')

# Start Jumping Jacks route
@app.route('/start_jumping_app', methods=['POST'])
def start_jumping_app():
    if request.method == 'POST':
        username = request.form.get('username')
        run_jumping_jack_app()
        return render_template('success.html')
    else:
        return render_template('error.html', error='Invalid request method')

# Stop Jumping Jacks route
@app.route('/stop_jumping_app', methods=['POST'])
def stop_jumping_app():
    stop_execution_internal()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
