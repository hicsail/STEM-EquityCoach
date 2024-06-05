from flask import request, jsonify
from app.main import main
from app.main import ollama

@main.route('/health', methods=['GET'])
def health():
    return jsonify(True)

@main.route('/inquire', methods=['POST'])
def inquire():
    try:
        data = request.get_json()
        question = data['question']
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        result = ollama.ask(question)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500