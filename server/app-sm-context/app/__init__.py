from flask import Flask
from app.services.ollama import create_ollama

def create_app():
    app = Flask(__name__)

    app.config['OLLAMA_INSTANCE'] = create_ollama()

    from app import routes
    app.register_blueprint(routes.bp)

    return app