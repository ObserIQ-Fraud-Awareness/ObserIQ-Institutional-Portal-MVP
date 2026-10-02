import os
from flask import Flask
from app.db.schema import close_db


def create_app(config_class="app.config.DevConfig"):
    """App factory"""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Resolve DATABASE filename into a full path inside backend/instance/
    app.config["DATABASE"] = os.path.join(app.instance_path, app.config["DATABASE"])

    # Create instance/ directory if missing
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Register database teardown
    app.teardown_appcontext(close_db)

    # TODO: Register blueprints routes are built

    return app