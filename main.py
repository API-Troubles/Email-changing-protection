import os
import re

import flask
import flask_login
from argon2 import PasswordHasher, exceptions
from flask import Flask, request, session
from flask_login import LoginManager, current_user
from replit import db


app = Flask(__name__, template_folder="site_files/")
hasher = PasswordHasher()

app.secret_key = os.environ['SECRET']

login_manager = LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.email)


@login_manager.user_loader
def load_user(email):
    info = db.get(email)
    return User(info["email"], info["password-hash"]) if info else None


@login_manager.unauthorized_handler
def unauthorized():
    print("unauthorized call")
    return flask.redirect(flask.url_for("login"))


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

        if db.get(email) is not None: # Ensure email is not taken
            return flask.make_response({"status": "Email taken"}, 409)

        # Create a user object
        db[email] = {"email": email, "password-hash": hasher.hash(password)}

        # Log in the new user!
        flask_login.login_user(User(db[email]["email"], db[email]["password-hash"]))
        return flask.make_response({"status": "OK"}, 201) # Return OK
    else: # Render signup page on GET req
        if current_user.is_authenticated:
            return flask.redirect(flask.url_for("settings"))
        else:
            return flask.render_template("signup.html")


@app.route('/login', methods = ['POST', 'GET']) # type: ignore
def login():
    if request.method == "POST":
        email = request.get_json().get("email")
        password = request.get_json().get("password")
        remember = request.get_json().get("remember-box") == "on" # Convert to bool

        # Checks
        if password is None or email is None:
            return flask.make_response({"status": "Missing data"}, 400)

        if db.get(email) is None:
            return flask.make_response({"status": "Incorrect username/password"}, 401)

        # Check if password is valid
        try:
            hasher.verify(db[email]["password-hash"], password)
        except exceptions.VerifyMismatchError:
            return flask.make_response({"status": "Incorrect username/password"}, 401)

        # Check if we need to rehash
        if hasher.check_needs_rehash(db[email]["password-hash"]):
            db[email] = {"email": email, "password-hash": hasher.hash(password)}

        flask_login.login_user(User(db[email]["email"], db[email]["password-hash"]), remember=remember)
        return flask.make_response({"status": "OK"}, 200)
    else: # Render login page on GET req
        if current_user.is_authenticated:
            return flask.redirect(flask.url_for("settings"))
        else:
            return flask.render_template("login.html")


@app.route('/change_email', methods=["GET"])
@flask_login.fresh_login_required
def change_email():
    email = request.args.get('email-field')
    if not email:
        return flask.make_response({"status": "No email"}, 400)
    if email_check.search(email) is None:
        return flask.make_response({"status": "Invalid email syntax"}, 400)

    return flask.render_template("change_email.html", email=email)


@app.route('/api/change_email', methods=["POST"])
@flask_login.fresh_login_required
def change_email_api():
    email = request.get_json().get('email')
    if not email:
        return flask.make_response({"status": "No email"}, 400)
    if email_check.search(email) is None:
        return flask.make_response({"status": "Invalid email syntax"}, 400)

    if not current_user.is_authenticated:
        return flask.make_response({"status": "Unauthorized"}, 401)

    # Write old email data to new email and delete orignal entry
    db[email] = db[current_user.email]
    print(f"Changing {current_user.email} => {email}")
    del db[current_user.email]

    return flask.render_template("logout.html") # Logout user afterwards


@app.route('/delete_account')
@flask_login.fresh_login_required
def delete_account():
    del db[flask_login.current_user.email]
    return flask.make_response("Account Deleted, bye!", 200)


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.render_template("logout.html")


@app.route('/settings')
@flask_login.fresh_login_required
def settings():
    return flask.render_template("settings.html", 
        user=flask_login.current_user
    )


@app.route('/about')
def about():
    return flask.render_template("about.html")

for i in db:
    print(f"Email: {i}")


app.run(host='0.0.0.0', port=8080, debug=True)
