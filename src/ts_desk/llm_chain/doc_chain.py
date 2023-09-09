import os
from langchain.vectorstores import Vectara
from langchain.vectorstores.vectara import VectaraRetriever
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.docstore.document import Document


class NormalChain:
    """
    For general topics like news, editorials etc.
    """
    def __init__(self, documents):
        self.documents = documents
        self.vectorstore = None
        self.qa = None

    def start_vector_instance(self):
        self.vectorstore = Vectara.from_documents(self.documents, embedding=None)

    def start_conversation_instance(self):
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        llm = OpenAI(openai_api_key=os.environ["openai_key"], temperature=0)
        retriever = self.vectorstore.as_retriever(lambda_val=0.025, k=5, filter=None)

        self.qa = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory)

    def doc_chain(self, question):
        try:
            result = self.qa({"question": question})
            print(result['answer'])
        except Exception as ex:
            print(ex)
            result = {'answer': "I couldn't find the answer"}

        return result['answer']
