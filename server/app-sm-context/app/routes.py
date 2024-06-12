from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('main', __name__)

@bp.route('/health', methods=['GET'])
def health():
    return jsonify(True)

@bp.route('/inquire', methods=['POST'])
def inquire():
    ollama = current_app.config['OLLAMA_INSTANCE']
    
    try:
        data = request.get_json()
        question = data['question']
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        result = ollama.ask(question)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500