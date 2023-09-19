import chromadb
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import uuid
import os
from pathlib import Path
from doc_chat.llm_chain.embedding_functions import SentenceTransformerEmbedding


class ChromaVectors:

    def __init__(self, session_id, document):
        self.chat_chain = None
        self.session_id = session_id
        self.document = document

    def create_client(self):
        self.chroma_client = chromadb.HttpClient(host="chroma", port=8000,
                                                 settings=Settings(allow_reset=True, anonymized_telemetry=False))

    def create_client_local(self):
        DIR = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(Path(DIR).parent, 'data')
        self.chroma_client = chromadb.PersistentClient(path=DB_PATH,
                                                       settings=Settings(allow_reset=True, anonymized_telemetry=False))

    def create_collection(self):
        self.document_collection = self.chroma_client.get_or_create_collection(name=self.session_id,
                                                                          embedding_function=SentenceTransformerEmbedding())

    def chroma_chain(self):
        self.chat_chain = Chroma(
            client=self.chroma_client,
            collection_name=self.session_id,
            embedding_function=SentenceTransformerEmbedding(),
        )

    def document_chunker(self):
        # split it into chunks
        text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=40)
        docs = text_splitter.split_documents([Document(page_content=self.document, metadata={'source': 'web'})])

        # define metadata
        ids = [str(uuid.uuid1()) for i in docs]
        metadatas = [{"source": "user"} for i in docs]

        return docs, ids, metadatas

    def collection(self):
        # chunk document and get metadatas
        docs, ids, metadatas = self.document_chunker()
        documents_to_add = [doc.page_content for doc in docs]

        # Add documents and embeddings to chromaDB
        self.document_collection.add(documents=documents_to_add, metadatas=metadatas, ids=ids)

    def delete_collection(self):
        self.chroma_client.delete_collection(self.session_id)

    def n_neighbours(self, question, n_results=3):
        results = self.document_collection.query(query_texts=question, n_results=n_results)
        context_to_use = results["documents"][0]
        return context_to_use

