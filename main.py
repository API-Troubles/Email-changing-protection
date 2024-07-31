from flask import Flask, render_template, request

from replit import db



app = Flask('app', template_folder="site_files/")

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        print(request.form.get("password-field"))
        return render_template("signup.html")

    elif request.method == 'GET':
        return render_template("signup.html")



app.run(host='0.0.0.0', port=8080, debug=True)
