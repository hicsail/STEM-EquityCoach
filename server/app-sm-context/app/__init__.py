import os

from flask import Flask
from app.main import main as main_blueprint
from app.services.ollama import Ollama

def create_app():
    app = Flask(__name__)
    
    global ollama
    ollama = Ollama()
    ollama.load_google_documents(id=os.getenv('GOOGLE_DRIVE_FOLDER_ID'))

    app.register_blueprint(main_blueprint)

    return app