from flask import Blueprint
from app.services.ollama import Ollama

main = Blueprint('main', __name__)

from app.main import routes