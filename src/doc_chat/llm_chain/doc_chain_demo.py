import os
from langchain.vectorstores import Vectara
from langchain.vectorstores.vectara import VectaraRetriever
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.memory import ConversationBufferMemory

# loader = TextLoader("../data/manipur.txt")
# documents = loader.load()

with open("../data/manipur.txt", 'r') as f:
    text = f.read()
metadata = {"source": "../data/manipur.txt"}
documents = [Document(page_content=text, metadata=metadata)]

vectorstore = Vectara.from_documents(documents, embedding=None)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

openai_api_key = os.environ["openai_key"]
llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
retriever = vectorstore.as_retriever(lambda_val=0.025, k=5, filter=None)

qa = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory)

# user_input = ''
print("starting chat with AI....")
user_input = input("Your question (type 'quit' to exit chat): ")

while user_input.lower() != 'quit':

    try:
        result = qa({"question": user_input})
        print(result['answer'])
    except Exception as ex:
        print(ex)

    user_input = input("Your question (type 'quit' to exit chat): ")