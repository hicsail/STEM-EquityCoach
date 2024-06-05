import os

from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.services.ollama import Ollama
    global ollama
    ollama = Ollama()
    ollama.load_google_documents(id=os.getenv('GOOGLE_DRIVE_FOLDER_ID'))

    return app