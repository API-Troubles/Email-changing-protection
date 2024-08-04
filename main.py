import os
import re

import flask
import flask_login
from argon2 import PasswordHasher, exceptions
from flask import Flask, request, session
from flask_login import LoginManager
from replit import db


app = Flask(__name__, template_folder="site_files/")
hasher = PasswordHasher()

app.secret_key = os.environ['SECRET']

login_manager = LoginManager()
login_manager.init_app(app)


# Test user db cause idk why nothing works rn
users = {}

class User(flask_login.UserMixin):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.email)


@login_manager.user_loader
def load_user(email):
    return users.get(email)


email_check = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')


# Obtain static files dymanically
@app.route('/static/js/<path:filepath>')
def get_js(filepath):
    return flask.send_from_directory('site_files/js/', filepath)

@app.route('/static/css/<path:filepath>')
def get_css(filepath):
    return flask.send_from_directory('site_files/css/', filepath)


# The actual parts of the site
@app.route('/')
def index():
    return flask.render_template("index.html")


@app.route('/signup', methods = ['POST', 'GET']) # type: ignore
def signup():
    if request.method == 'POST':
        email = request.get_json().get("email")
        password = request.get_json().get("password")

        # Checks
        if password is None or email is None: # Ensure pw/email exist
            return flask.make_response({"status": "Missing data"}, 400)
        if email_check.search(email) is None: # Ensure email matches regex
            return flask.make_response({"status": "Invalid Email"}, 400)

        if users.get(email) is not None: # Ensure email is not taken
            return flask.make_response({"status": "Email taken"}, 409)

        # Create a user object
        users[email] = User(email, hasher.hash(password))

        # Log in the new user!
        flask_login.login_user(users[email])
        return flask.make_response({"status": "OK"}, 201) # Return OK
    else: # Render signup page on GET req
        if session.get('email'):
            return flask.render_template("settings.html")
        return flask.render_template("signup.html")


@app.route('/login', methods = ['POST', 'GET']) # type: ignore
def login():
    if request.method == "POST":
        email = request.form.get("email-field")
        password = request.form.get("password-field")
        remember = request.form.get("remember-me")

        # Checks
        if password is None or email is None:
            return flask.make_response({"status": "Missing data"}, 400)

        if users.get(email) is None:
            return flask.make_response({"status": "Incorrect username/password"}, 401)

        # Check if password is valid
        try:
            hasher.verify(users[email]["password-hash"], password)
        except exceptions.VerifyMismatchError:
            return flask.make_response({"status": "Incorrect username/password"}, 401)

        # Check if we need to rehash
        if hasher.check_needs_rehash(users[email]["password-hash"]):
            users[email]["password-hash"] = hasher.hash(password)

        print(users.get(email))

        flask_login.login_user(users.get(email)) # Login a user
        return flask.make_response({"status": "OK"}, 200)
    else: # Render login page on GET req
        if session.get('email'):
            return flask.render_template("settings.html")
        return flask.render_template("login.html")


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.render_template("logout.html")


@app.route('/settings')
@flask_login.login_required
def settings():
    print(flask_login.current_user)
    return flask.render_template_string(
        "logged in as: {{ user.id }}", 
        user=flask_login.current_user
    )


@app.route('/about')
def about():
    return flask.render_template("about.html")


for i in users:
    print(f"Email: {i}")


app.run(host='0.0.0.0', port=8080, debug=True)
