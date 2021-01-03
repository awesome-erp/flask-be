from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    origins = "*"

    CORS(app,
         origins=origins,
         expose_headers='Authorization',
         supports_credentials=True,
         allow_headers=['Access-Control-Allow-Origin',
                        'Access-Control-Allow-Methods',
                        'Access-Control-Allow-Origin',
                        'Authorization',
                        'sessionId',
                        "Access-Control-Allow-Headers",
                        "Content-Type"
                        ])

    from aerp.modules.auth import authorization

    # Register blueprints
    app.register_blueprint(authorization, url_prefix='/auth')

    return app
