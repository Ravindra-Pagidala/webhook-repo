from flask import Flask
from dotenv import load_dotenv
from app.extensions import init_mongo
from app.controllers.webhook_controller import webhook_bp
from app.controllers.ui_controller import ui_bp

load_dotenv()  # Load .env file

def create_app():
    app = Flask(__name__)

    # Initialize MongoDB
    init_mongo(app)

    # Register blueprints
    app.register_blueprint(webhook_bp)
    app.register_blueprint(ui_bp)

    return app
