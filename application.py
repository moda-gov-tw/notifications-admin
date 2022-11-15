from flask import Flask, g
from flask_babel import Babel

from app import create_app

application = Flask("app")

create_app(application)

babel = Babel(application)
babel.app.config["BABEL_TRANSLATION_DIRECTORIES"] = "locales"


@babel.localeselector
def get_locale():
    return getattr(g, "LOCALE", "zh_Hant_TW")
