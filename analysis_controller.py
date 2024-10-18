from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from os_process import chat_ollama_single_stream,  extract_message_from_stream, chat_ollama_single_stream_1, generate_sample_stream_data

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

@app.route('/chat-single-stream', methods=['POST'])
def chat_single_stream():
    data = request.json
    print(data)
    query = data['query']

    # Stream the response back in bytes
    return Response(chat_ollama_single_stream_1(query), content_type='text/plain; charset=utf-8')

@app.route('/chat-single-stream-sample', methods=['POST'])
def chat_single_stream_sample():
    # Optionally handle the POST request data
    data = request.form.to_dict()
    print(f"Received POST data: {data}")

    # Return a streaming response
    return Response(generate_sample_stream_data(), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=9876, host="0.0.0.0")
