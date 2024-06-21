import os
import time

from dotenv import load_dotenv

from langchain_community.llms import Ollama as OllamaBase
from langchain_google_community import GoogleDriveLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

import google_drive
import utils

import warnings
from langchain._api import LangChainDeprecationWarning  # TODO: can be removed in the future

warnings.simplefilter('ignore', LangChainDeprecationWarning)    # TODO: can be removed in the future

SYSTEM_TEMPLATE = """
Answer the user's question based on the context below. If the context doesn't contain any relevant information to the question, say you don't know. Do not make up information.

<context>{context}</context>
"""
CHROMA_PATH = './chroma'
DOWNLOAD_BATCH_SIZE = 3

qa_prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_TEMPLATE), ("human", "{input}")]
)

class Ollama:
    def __init__(self):
        load_dotenv()

        self.ollama = OllamaBase(base_url=os.getenv('OLLAMA_URL'), model='llama2')
        self.google = google_drive.GoogleDriveClient()
        self.chroma_init()

    def chroma_init(self):
        timestart = time.time()
        if os.path.exists(CHROMA_PATH):
            print('Chroma already exists. Loading...')
            self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=GPT4AllEmbeddings())
            self.retriever = self.db.as_retriever(search_kwargs={'k': 4})
            self.qa_chain = create_stuff_documents_chain(self.ollama, qa_prompt)
        else:
            print('Initializing Chroma...')
            self.db = Chroma(embedding_function=GPT4AllEmbeddings(), persist_directory=CHROMA_PATH)
            self.retriever = self.db.as_retriever(search_kwargs={'k': 4})
            self.qa_chain = create_stuff_documents_chain(self.ollama, qa_prompt)
        timeend = time.time()

        print('Time taken to initialize Chroma: ', timeend - timestart, 'seconds')

    def __split_and_add(self, data, chunk_size=500, chunk_overlap=10):
        if not data:
            return

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(data)
        max_batch_size = 5461

        for i in range(0, len(chunks), max_batch_size):
            batch = chunks[i:i + max_batch_size]
            self.db.add_documents(batch)
            print(f'Batch {i // max_batch_size + 1} added, size: {len(batch)}')
            
        # if not os.path.exists(CHROMA_PATH):
        #     self.db = Chroma.from_documents(chunks, GPT4AllEmbeddings(), persist_directory=CHROMA_PATH)
        #     self.retriever = self.db.as_retriever(search_kwargs={'k': 4})
        #     self.qa_chain = create_stuff_documents_chain(self.ollama, qa_prompt)
        # else:
        #     self.db.add_documents(chunks)

    def load_google_drive(self, id, chunk_size=500, chunk_overlap=10):
        timestart = time.time()

        # Loading PDFs from Google Drive
        print('Loading PDFs from Google Drive...')
        loader = GoogleDriveLoader(folder_id=id, recursive=True, service_account_key=os.getenv('GOOGLE_CREDS_PATH'))
        data = loader.load()
        
        self.__split_and_add(data, chunk_size, chunk_overlap)
        print('PDFs loaded')

        # Load other files from Google Drive
        files, compressed_files = self.google.get_file_ids(id, ignore_ext=['pdf'])

        # Download/extract/load compressed files
        for file in compressed_files:
            print('Downloading and extracting compressed file...')
            path, meta = self.google.download_file(file)
            extracted_path = utils.extract_file(path)
            loader = PyPDFDirectoryLoader(extracted_path)
            data = loader.load()
            self.__split_and_add(data, chunk_size, chunk_overlap)
            print(f'Compressed file {meta["name"]} loaded')

            # Delete extracted files
            utils.remove_directory(extracted_path)
            print('Extracted files deleted')

        # Download and load other files to Chroma
        cnt = DOWNLOAD_BATCH_SIZE
        batch = 0
        print('Downloading and loading other files...')
        while files:
            file_id = files.pop()
            path, _ = self.google.download_file(file_id)
            cnt -= 1

            if cnt == 0 or not files:
                print(f'Batch {batch} loaded')
                batch += 1
                cnt = DOWNLOAD_BATCH_SIZE
                loader = PyPDFDirectoryLoader(os.getenv('DOWNLOAD_PATH'))
                data = loader.load()
                self.__split_and_add(data, chunk_size, chunk_overlap)
                print(f'Batch {batch} loaded')

                # remove everything in the download path
                utils.clear_directory(os.getenv('DOWNLOAD_PATH'))
                print('Download path cleared')

        timeend = time.time()
        print('Time taken to load documents: ', timeend - timestart, 'seconds')
    
    def ask(self, question, print_result = False):
        chain = create_retrieval_chain(self.retriever, self.qa_chain)
        result = chain.invoke({'input': question})

        if print_result:
            print('\033[92m' + 'Input:' + '\033[97m', result['input'] + '\033[0m')
            print('\033[92m' + 'Answer:' + '\033[97m', result['answer'] + '\033[0m')
            print('\033[92m' + 'Context:' + '\033[97m', str(result['context']) + '\033[0m')
        