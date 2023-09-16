from flask import Flask, render_template, request, jsonify
from doc_chat.llm_chain.doc_chain import ChromaChain
import os

app = Flask(__name__)
dataFolder = "uploaded_data"

global chain_instance
chain_instance = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/message', methods=['POST'])
def receive_message():
    message = request.form.get('message')
    if message:
        if not chain_instance:
            return jsonify({"reply": "Hi there! Please upload a valid file before proceeding"})
        else:
            reply = chain_instance.doc_chain(message)
            return jsonify({"reply": reply})
    return jsonify({"reply": "No message received"})


@app.route('/upload', methods=['POST'])
def upload_file():
    # print(request.files)
    if 'file' in request.files:
        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
            text = uploaded_file.read()
            print(text)
            metadata = {"source": uploaded_file.filename}
            documents = text

            global chain_instance
            chain_instance = ChromaChain(documents)
            chain_instance.start_vector_instance()
            chain_instance.start_conversation_instance()

            follow_up_message = f"I have understood the document. \n Please shoot your questions."
            return jsonify({"status": "File uploaded successfully", "follow_up_message": follow_up_message})
    return jsonify({"status": "File upload failed", "follow_up_message": "File upload failed"})


if __name__ == '__main__':
    app.run(debug=True)
