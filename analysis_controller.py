from flask import Flask, request, jsonify
from flask_cors import CORS
from os_process import chat_ollama_single_stream,  extract_message_from_stream

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return 'Server is up and running!', 200

@app.route('/chat-single', methods=['POST'])
def chat_single():
    data = request.json
    print(data)
    query = data['query']
    stream = chat_ollama_single_stream(query)
    output = extract_message_from_stream(stream)
    print(output)
    return jsonify({'llm_output': output}), 200

if __name__ == '__main__':
    app.run(debug=True)
