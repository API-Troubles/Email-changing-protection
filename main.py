import os
import re

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
from replit import db

app = Flask(__name__, template_folder="site_files/")
hasher = PasswordHasher()

app.secret_key = os.environ['SECRET']

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
        email = request.form.get("email-field")
        password = request.form.get("password-field")
        re_password = request.form.get("re-password-field")

        # Checks
        if password is None or re_password is None or email is None:
            return make_response("Invalid Data", 400)
        if password != re_password:
            return make_response("Invalid Data", 400)
        if email_check.search(email) is None:
            return make_response("Invalid Data", 400)

        if db.get(email) is not None:
            return "email taken"

        db["email"] = {
            "password-hash": hasher.hash(password)
        }
        session['email'] = email
        return redirect(url_for('settings'))
    else: # Render signup page on GET req
        return render_template("signup.html")


@app.route('/login', methods = ['POST', 'GET']) # type: ignore
def login():
    if request.method == "POST":
        email = request.form.get("email-field")
        password = request.form.get("password-field")

        # Checks
        if password is None or email is None:
            return make_response("Invalid Data", 400)

        if db.get(email) is None:
            return make_response("Email not found", 400)

        # Check if password is valid
        try:
            hasher.verify(db[email]["password-hash"], password)
        except exceptions.VerifyMismatchError:
            return make_response("Unauthorized", 401)

        # Check if we need to rehash
        if hasher.check_needs_rehash(db[email]["password-hash"]):
            db[email]["password-hash"] = hasher.hash(password)

        return redirect(url_for("settings"))
    else: # Render login page on GET req
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/settings')
def settings():
    return "settings"


@app.route('/about')
def about():
    return render_template("about.html")


app.run(host='0.0.0.0', port=8080, debug=True)
