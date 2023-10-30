from langchain.text_splitter import CharacterTextSplitter
import uuid
from langchain.docstore.document import Document


class BaseClient:
    """
    Parent class for all vector store classes
    """

    def __init__(self, session_id, document):
        self.__session_id = session_id
        self.__document = document

    @property
    def session(self):
        return self.__session_id

    @property
    def document(self):
        return [Document(page_content=self.__document, metadata={'source': 'web'})]
    
    def document_chunker(self):
        # split it into chunks
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=40)
        docs = text_splitter.split_documents(self.document)

        # define metadata
        ids = [str(uuid.uuid1()) for i in docs]
        metadatas = [{"source": "user"} for i in docs]

        return docs, ids, metadatas
