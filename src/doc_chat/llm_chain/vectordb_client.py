import chromadb
from chromadb.config import Settings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import uuid


class ChromaVectors:

    def __init__(self, session_id, document):
        self.chat_chain = None
        self.session_id = session_id
        self.document = document

    def create_client(self):
        self.chroma_client = chromadb.HttpClient(host="chroma", port=8000,
                                                 settings=Settings(allow_reset=True, anonymized_telemetry=False))

    def create_collection(self):
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.document_collection = self.chroma_client.get_or_create_collection(name=self.session_id,
                                                                          embedding_function=embedding_function)

    def chroma_chain(self):
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.chat_chain = Chroma(
            client=self.chroma_client,
            collection_name=self.session_id,
            embedding_function=embedding_function,
        )

    def document_chunker(self):
        # split it into chunks
        text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=40)
        docs = text_splitter.split_documents([Document(page_content=self.document, metadata={'source': 'web'})])

        # define metadata
        ids = [uuid.uuid1() for i in docs]
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
        results = self.document_collection.query(question, n_results=n_results)
        context_to_use = '; '.join(results["documents"])
        return context_to_use
