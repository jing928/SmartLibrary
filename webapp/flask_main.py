# pip3 install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy
# python3 flask_main.py
import os
from flask import Flask
from flask_bootstrap import Bootstrap

from flask_api import api, db
from flask_site import site
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)

basedir = os.path.abspath(os.path.dirname(__file__))

# Parameter to connect to GCP SQL DB
HOST = "35.189.0.166"
USER = "root"
PASSWORD = "password"
DATABASE = "SmartLibrary"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)

if __name__ == "__main__":
    app.run(host=Config.HOST_IP, debug=True)
