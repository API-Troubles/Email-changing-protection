import re
import os

from argon2 import PasswordHasher
from flask import (
    Flask,
    make_response,
    render_template,
    request,
    send_from_directory,
    url_for,
    redirect,
    session
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


@app.route('/signup', methods = ['POST']) # type: ignore
def signup():
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

    db[email] = {
        "password-hash": hasher.hash(password)
    }
    session['email'] = email
    return redirect(url_for('settings'))


@app.route('/login', methods = ['POST']) # type: ignore
def login():
    email = request.form.get("email-field")
    password = request.form.get("password-field")

    # Checks
    if password is None or email is None:
        return make_response("Invalid Data", 400)


    if hasher.verify(db[email], password):
        session['email'] = email
        return redirect(url_for('settings'))



app.run(host='0.0.0.0', port=8080, debug=True)
