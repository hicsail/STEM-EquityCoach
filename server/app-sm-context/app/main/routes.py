from flask import jsonify
from app.main import main

@main.route('/health', methods=['GET'])
def health():
    return jsonify(True)