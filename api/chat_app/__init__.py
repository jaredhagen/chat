import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        CHAT_DYNAMODB_TABLE_NAME=os.getenv('CHAT_DYNAMODB_TABLE_NAME'),
        CHAT_DYNAMODB_LOCALHOST_PORT=os.getenv('CHAT_DYNAMODB_LOCALHOST_PORT')
    )

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
