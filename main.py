from argon2 import PasswordHasher
from flask import Flask, make_response, render_template, request, send_from_directory
from replit import db

app = Flask(__name__, template_folder="site_files/")
hasher = PasswordHasher()


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


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email-field")
        password = request.form.get("password-field")
        re_password = request.form.get("re-password-field")

        # Checks
        if password is None or re_password is None:
            return make_response("Invalid Data", 400)
        if password != re_password:
            return make_response("Invalid Data", 400)

        password_hashed = hasher.hash(password)
        return render_template("signup.html")

    elif request.method == 'GET':
        return render_template("signup.html")



app.run(host='0.0.0.0', port=8080, debug=True)
