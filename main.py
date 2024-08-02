from dataclasses import is_dataclass
import os
import re

import uuid

from argon2 import PasswordHasher, exceptions
from flask import (
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_login import LoginManager
import flask_login
from replit import db

app = Flask(__name__, template_folder="site_files/")
hasher = PasswordHasher()

app.secret_key = os.environ['SECRET']

login_manager = LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(email):
    return db.get(email)



email_check = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')


# Obtain static files dymanically
@app.route('/static/js/<path:filepath>')
def get_js(filepath):
    return send_from_directory('site_files/js/', filepath)

@app.route('/static/css/<path:filepath>')
def get_css(filepath):
    return send_from_directory('site_files/css/', filepath)


# The actual parts of the site
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods = ['POST', 'GET']) # type: ignore
def signup():
    if request.method == 'POST':
        email = request.get_json().get("email")
        password = request.get_json().get("password")

        # Checks
        if password is None or email is None: # Ensure pw/email exist
            return make_response({"status": "Missing data"}, 400)
        if email_check.search(email) is None: # Ensure email matches regex
            return make_response({"status": "Invalid Email"}, 400)

        if db.get(email) is not None: # Ensure email is not taken
            return make_response({"status": "Email taken"}, 409)

        # Create a user object with a unique UUID
        db[email] = User(email, hasher.hash(password))

        flask_login.login_user(User(email, hasher.hash(password)))
        return make_response({"status": "OK"}, 201) # Return OK
    else: # Render signup page on GET req
        if session.get('email'):
            return render_template("settings.html")
        return render_template("signup.html")


@app.route('/login', methods = ['POST', 'GET']) # type: ignore
def login():
    if request.method == "POST":
        email = request.form.get("email-field")
        password = request.form.get("password-field")
        remember = request.form.get("remember-me")

        user = db.get(email)

        # Checks
        if password is None or email is None:
            return make_response({"status": "Missing data"}, 400)

        if db.get(email) is None:
            return make_response({"status": "Incorrect username/password"}, 401)

        # Check if password is valid
        try:
            hasher.verify(db[email]["password-hash"], password)
        except exceptions.VerifyMismatchError:
            return make_response({"status": "Incorrect username/password"}, 401)

        # Check if we need to rehash
        if hasher.check_needs_rehash(db[email]["password-hash"]):
            db[email]["password-hash"] = hasher.hash(password)

        flask_login.login_user(email) # Login a user
        return make_response({"status": "OK"}, 200)
    else: # Render login page on GET req
        if session.get('email'):
            return render_template("settings.html")
        return render_template("login.html")


@app.route('/logout')
@flask_login.login_required
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/settings')
@flask_login.login_required
def settings():
    return "settings"


@app.route('/about')
def about():
    return render_template("about.html")


app.run(host='0.0.0.0', port=8080, debug=True)
