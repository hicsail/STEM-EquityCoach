import os
import time

from langchain_community.llms import Ollama as OllamaBase
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_google_community import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain

SERVICE_ACCOUNT_FILE = '/root/.credentials/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

CHROMA_PATH = './chroma'
SYSTEM_TEMPLATE = """
Answer the user's question based on the context below. If the context doesn't contain any relevant information to the question, say you don't know. Do not make up information.

<context>{context}</context>
"""

class Ollama:
    def __init__(self):
        self.ollama = OllamaBase(base_url=os.getenv('OLLAMA_URL'), model='llama2')
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [("system", SYSTEM_TEMPLATE), ("human", "{input}")]
        )

        self.__chroma_init()

    def __chroma_init(self):
        timestart = time.time()

        if os.path.exists(CHROMA_PATH):
            print('Chroma already exists. Loading...')
            # self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=GPT4AllEmbeddings())
            self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OllamaEmbeddings(base_url=os.getenv('OLLAMA_URL')))
            self.retriever = self.db.as_retriever(search_kwargs={'k': 4})
            self.qa_chain = create_stuff_documents_chain(self.ollama, self.qa_prompt)
        
        timeend = time.time()

        print('Time taken to initialize Chroma: ', timeend - timestart, 'seconds')

    def load_google_documents(self, id, recursive=True, chunk_size=500, chunk_overlap=10):
        timestart = time.time()

        print('Loading documents from Google Drive...')
        if id:
            loader = GoogleDriveLoader(folder_id=id, recursive=recursive, service_account_key=SERVICE_ACCOUNT_FILE)
            data = loader.load()
        else:
            raise ValueError('No folder id provided')
        
        self.__split_and_add(data, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        timeend = time.time()

        print('Time taken to load documents: ', timeend - timestart, 'seconds')
        
    def __split_and_add(self, data, chunk_size=500, chunk_overlap=10):
        print('Splitting and adding documents...')
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        print('Splitting documents...')
        chunks = text_splitter.split_documents(data)

        print('Checking if Chroma exists...')
        if not os.path.exists(CHROMA_PATH):
            print('Chroma does not exist. Creating...')
            # self.db = Chroma.from_documents(chunks, GPT4AllEmbeddings(), persist_directory=CHROMA_PATH)
            self.db = Chroma.from_documents(chunks, OllamaEmbeddings(base_url=os.getenv('OLLAMA_URL')), persist_directory=CHROMA_PATH)
            print('Creating retriever...')
            self.retriever = self.db.as_retriever(search_kwargs={'k': 4})
            print('Creating QA chain...')
            self.qa_chain = create_stuff_documents_chain(self.ollama, self.qa_prompt)
        else:
            print('Chroma exists. Adding documents...')
            self.db.add_documents(chunks)

    def ask(self, question, print_result=False):
        chain = create_retrieval_chain(self.retriever, self.qa_chain)
        result = chain.invoke({'input': question})

        if print_result:
            print('\033[92m' + 'Input:' + '\033[97m', result['input'] + '\033[0m')
            print('\033[92m' + 'Answer:' + '\033[97m', result['answer'] + '\033[0m')
            print('\033[92m' + 'Context:' + '\033[97m', str(result['context']) + '\033[0m')

        return result
    
def create_ollama():
    global ollama_instance
    if 'ollama_instance' not in globals():
        ollama_instance = Ollama()
        ollama_instance.load_google_documents(id=os.getenv('GOOGLE_DRIVE_FOLDER_ID'))
        
        return ollama_instance