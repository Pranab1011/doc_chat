from flask import Flask, request, jsonify
import chromadb
from chromadb.config import Settings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import uuid

app = Flask(__name__)


@app.route('/store', methods=['POST'])
def store_data():
    try:
        # Get data from the POST request's JSON payload
        request_data = request.get_json()

        if 'session_id' not in request_data or 'document' not in request_data:
            return jsonify({"error": "Missing 'session_id' or 'document' in request data"}), 400

        session_id = request_data['session_id']
        document = request_data['document']

        # split it into chunks
        text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=40)
        docs = text_splitter.split_documents(document)

        # define metadata
        ids = [uuid.uuid1() for i in docs]
        metadatas = [{"source": "user"} for i in docs]

        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        chroma_client = chromadb.HttpClient(host="chroma", port=8000,
                                            settings=Settings(allow_reset=True, anonymized_telemetry=False))
        document_collection = chroma_client.get_or_create_collection(name=session_id,
                                                                     embedding_function=embedding_function)
        document_collection.add(documents=docs, metadatas=metadatas, ids=ids)

        return jsonify({"message": "Data stored successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/retrieve/<key>', methods=['GET'])
def retrieve_data(key):
    try:
        # Check if the key exists in the data dictionary
        if key in data:
            return jsonify({"value": data[key]})
        else:
            return jsonify({"message": "Key not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
