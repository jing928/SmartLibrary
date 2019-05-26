"""
This module provides program entry point to run the flask web part.
It includes: 1. API part - api 2. Website part - site
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_api import api, db
from flask_site import site


class RunFlask:
    """
    The RunFlask class wraps all the componets and configurations required 
    for flask website.
    It provides the method to start the entire Flask website.
    """

    def __init__(self):
        """Initialize the website with proper configuration parameters
        Including:
            DB connection string,
            Bootstrap,
            Blueprint registration,
            Hosting IP address.

        Returns:
            None

        """
        self.app = Flask(__name__)
        self.bootstrap = Bootstrap(self.app)
        self.app.config.from_object(Config)

        # Parameter to connect to GCP SQL DB
        self.host = Config.DATABASE_CONFIG['HOST']
        self.user = Config.DATABASE_CONFIG['USER']
        self.password = Config.DATABASE_CONFIG['PASSWORD']
        self.database = Config.DATABASE_CONFIG['DATABASE']

        self.app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(
            self.user, self.password, self.host, self.database)
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        db.init_app(self.app)

        self.app.register_blueprint(api)
        self.app.register_blueprint(site)

    @staticmethod
    def run():
        """Fires up the Flask website.

        It starts the flask website on the Master Pi.

        Returns:
            None

        """
        flask = RunFlask()
        flask.app.run(host=Config.HOST_IP, debug=True)


if __name__ == "__main__":
    RunFlask.run()
