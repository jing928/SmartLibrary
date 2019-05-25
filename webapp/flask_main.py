from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_api import api, db
from flask_site import site


class RunFlask:
    def __init__(self):
        self.app = Flask(__name__)
        self.bootstrap = Bootstrap(self.app)
        self.app.config.from_object(Config)
        # basedir = os.path.abspath(os.path.dirname(__file__))

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
        flask = RunFlask()
        flask.app.run(host=Config.HOST_IP, debug=True)


if __name__ == "__main__":
    RunFlask.run()
