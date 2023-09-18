from flask import Flask, render_template, request, jsonify, session
from doc_chat.llm_chain.doc_chain import ChromaChain
from flask_session import Session
import os

app = Flask(__name__)
# app.config['PERMANENT_SESSION_LIFETIME'] = 1800
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/app/doc_chat/data/session_data'  # Use an appropriate subdirectory
app.config['SESSION_PERMANENT'] = False  # Session will expire when the browser is closed

Session(app)


@app.route('/')
def index():
    if 'session_id' not in session:
        # Generate a session-specific ID and store it in the session
        session['session_id'] = session.sid
        print("session id: ", session['session_id'])
    return render_template('index.html')


@app.route('/message', methods=['POST'])
def receive_message():
    message = request.form.get('message')
    if message:
        if not session["chain_instance"]:
            return jsonify({"reply": "Hi there! Please upload a valid file before proceeding"})
        else:
            chain_instance = session["chain_instance"]
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

            chain_instance = ChromaChain(documents, session['session_id'])
            chain_instance.start_vector_instance()
            chain_instance.start_conversation_instance()
            session["chain_instance"] = chain_instance

            follow_up_message = f"I have understood the document. \n Please shoot your questions."
            return jsonify({"status": "File uploaded successfully", "follow_up_message": follow_up_message})
    return jsonify({"status": "File upload failed", "follow_up_message": "File upload failed"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
