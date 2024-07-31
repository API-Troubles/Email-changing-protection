from flask import Flask
from flask import render_template

from replit import db




app = Flask('app', template_folder="site_files/")

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
  return "hi"

app.run(host='0.0.0.0', port=8080, debug=True)
