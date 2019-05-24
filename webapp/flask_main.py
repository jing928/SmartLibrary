# pip3 install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy
# python3 flask_main.py
import os
from flask import Flask
from flask_bootstrap import Bootstrap

from flask_api import api, db
from flask_site import site
from config import Config

class RunFlask:
    def __init__(self):
        self.app = Flask(__name__)
        self.bootstrap = Bootstrap(self.app)
        self.app.config.from_object(Config)
        # basedir = os.path.abspath(os.path.dirname(__file__))

        # Parameter to connect to GCP SQL DB
        self.HOST = Config.DATABASE_CONFIG['HOST']
        self.USER = Config.DATABASE_CONFIG['USER']
        self.PASSWORD = Config.DATABASE_CONFIG['PASSWORD']
        self.DATABASE = Config.DATABASE_CONFIG['DATABASE']

        self.app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(
            self.USER, self.PASSWORD, self.HOST, self.DATABASE)
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        db.init_app(self.app)

        self.app.register_blueprint(api)
        self.app.register_blueprint(site)

    def run(self):
        self.app.run(host=Config.HOST_IP, debug=True)

if __name__ == "__main__":
    flask = RunFlask()
    flask.run()
