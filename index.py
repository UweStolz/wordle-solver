from os import environ
from flask import Flask
from dotenv import load_dotenv

from logger import logger
from routes import api

load_dotenv(verbose=True)

ENVIRONMENT = environ.get("FLASK_ENV")
app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    if ENVIRONMENT == "development":
        app.run(debug=True)
        logger.enable("__main__")
    else:
        logger.disable("__main__")
    pass
