import os
from langchain.vectorstores import Vectara
from langchain.vectorstores.vectara import VectaraRetriever
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.docstore.document import Document
from doc_chat.llm_chain.vectordb_client import ChromaVectors
import yaml

with open('../configs/llm_config.yml', 'r') as file:
    configs = yaml.safe_load(file)


class VectaraChain:
    """
    For Vectara vectore store.
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


class ChromaChain:
    """
    For Chroma DB vectore store.
    """
    def __init__(self, documents, session_id):
        self.documents = documents
        self.vectorstore = None
        self.qa = None
        self.session_id = session_id

    def start_vector_instance(self):
        self.vectorstore = ChromaVectors(self.session_id, self.documents)
        self.vectorstore.create_client()
        self.vectorstore.create_collection()
        self.vectorstore.collection()

    def start_conversation_instance(self):
        # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.llm = OpenAI(openai_api_key=os.environ["openai_key"], temperature=0.2)

    def doc_chain(self, question):
        context = self.vectorstore.n_neighbours(question=question, n_results=3)
        template = configs["rag_template_n_3"]
        prompt = f"{template} \n Q={question} \n doc_1={context[0]} \n doc_2={context[1]} \n doc_2={context[2]}"

        try:
            reply = self.llm(prompt)
            print(reply)
        except Exception as ex:
            print(ex)
            reply = "I couldn't find the answer"

        return reply

