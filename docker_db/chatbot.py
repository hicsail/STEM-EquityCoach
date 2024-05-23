import uuid

from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

import chromadb
from chromadb.config import Settings

import warnings
from langchain._api import LangChainDeprecationWarning  # TODO: can be removed in the future

warnings.simplefilter('ignore', LangChainDeprecationWarning)    # TODO: can be removed in the future

SYSTEM_TEMPLATE = """
Answer the user's question based on the context below. If the context doesn't contain any relevant information to the question, say you don't know. Do not make up information.

<context>{context}</context>
"""
CHROMA_PATH = 'chroma'
DOC_PATH = 'res'

qa_prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_TEMPLATE), ("human", "{input}")]
)

class ChatBot:
    def __init__(self):
        self.ollama = Ollama(base_url='http://localhost:11434', model='llama2')
        self.chroma_init()

    def chroma_init(self):
        self.client = chromadb.HttpClient(host="localhost", port=8000, settings=Settings(allow_reset=True))
        self.client.reset()

        self.collection = self.client.create_collection('my_collection')

        self.db4 = Chroma(client=self.client, collection_name='my_collection', embedding_function=GPT4AllEmbeddings())
        # self.retriever = self.db4.as_retriever(search_kwargs={'k': 4})
        self.qa_chain = create_stuff_documents_chain(self.ollama, qa_prompt)

    # def __get_chroma(self, chunks, k = 4, chroma_path = CHROMA_PATH):
    #     if os.path.exists(chroma_path):
    #         vectorstore = Chroma(persist_directory=chroma_path, embedding_function=GPT4AllEmbeddings())
    #     else:
    #         vectorstore = Chroma.from_documents(chunks, embedding=GPT4AllEmbeddings(), persist_directory=chroma_path)    

    #     return vectorstore.as_retriever(search_kwargs={'k': k})

    def load_documents(self, file_path, chunk_size=500, chunk_overlap=10):
        if file_path:
            loader = PyPDFLoader(file_path)
            data = loader.load()
        else:
            raise ValueError('No file or directory path provided')
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(data)

        for chunk in chunks:
            self.collection.add(
                ids=[str(uuid.uuid4())],
                metadatas=[chunk.metadata],
                documents=[chunk.page_content]
            )
    
    def ask(self, question, print_result = False):
        # docs = self.db4.similarity_search(question, k=4)
        chain = create_retrieval_chain(self.retriever, self.qa_chain)
        result = chain.invoke({'input': question})

        if print_result:
            print('\033[92m' + 'Input:' + '\033[0m', result['input'])
            print('\033[92m' + 'Answer:' + '\033[0m', result['answer'])
            print('\033[92m' + 'Context:' + '\033[0m', result['context'])
    