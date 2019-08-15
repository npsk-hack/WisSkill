from flask import Flask,send_from_directory

app = Flask(__name__, template_folder='templates',static_url_path='/css/styles.css')

from app import routes

app.run(debug=True)