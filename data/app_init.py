import os

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
    )
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    app.config.from_pyfile("config.py", silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from data import db
    db.init_app(app)

    from data import blueprints_user
    from data import blueprints_competiton
    app.register_blueprint(blueprints_user.bp)
    app.register_blueprint(blueprints_competiton.bp)

    return app
