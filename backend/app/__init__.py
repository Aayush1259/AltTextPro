from flask import Flask
from app.api.routes import bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # CORS(app)  # Enable CORS for all routes
    app.register_blueprint(bp)
    return app