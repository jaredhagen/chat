import os

from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        CHAT_DYNAMODB_ENDPOINT_URL="http://dynamodb:8000",
        CHAT_DYNAMODB_TABLE_NAME=os.getenv("CHAT_DYNAMODB_TABLE_NAME"),
    )

    # In a real world scenario I'd be more intentional about what
    # origins I'd allow requests from.  Ideally this would be
    # easily configureable with environment variables or based on what
    # environment the app is running in.
    CORS(app, origins="*")

    if test_config:
        app.config.from_mapping(test_config)

    from . import errors

    errors.register_error_handlers(app)

    from . import users

    app.register_blueprint(users.bp)

    from . import rooms

    app.register_blueprint(rooms.bp)

    from . import messages

    app.register_blueprint(messages.bp)

    return app
