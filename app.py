from flask import Flask, request, jsonify
from flask_cors import CORS
from models import save_data, retrieve_documents
import cohere

app = Flask(__name__)
CORS(app)
# Initialize the Cohere client
COHERE_API_KEY = 'ICA5iYm35snU81dBBCzHTSxy7mVKLOALUCQfQCnL'
co = cohere.Client(COHERE_API_KEY)

@app.route('/train', methods=['POST'])
def train():
    data = request.get_json()
    if not data or 'patientId' not in data or 'data' not in data:
        return jsonify({"error": "patientId and data fields are required"}), 400
    save_data(data['patientId'], data['data'])
    return jsonify({"message": "Data saved."})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if not data or 'patientId' not in data or 'question' not in data:
        return jsonify({"error": "patientId and question fields are required"}), 400
    patientId = data['patientId']
    question = data['question']
    documents = retrieve_documents(patientId)
    answer = generate_response(question, documents)
    return jsonify({"answer": answer})

def generate_response(question, documents):
    response_stream = co.chat_stream(
        message=question,
        documents=documents,
        
    )
    generated_text = ""
    for token in response_stream:
        if hasattr(token, 'text'):
            generated_text += token.text
    return generated_text

if __name__ == '__main__':
    app.run(debug=True, port=5000)