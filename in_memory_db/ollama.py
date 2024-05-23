import os

from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

SYSTEM_TEMPLATE = """
Answer the user's question based on the context below. If the context doesn't contain any relevant information to the question, say you don't know. Do not make up information.

<context>{context}</context>
"""
CHROMA_PATH = 'chroma'
DOC_PATH = 'res'

qa_prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_TEMPLATE), ("human", "{input}")]
)

# load and prepare the documents
loader = PyPDFDirectoryLoader(DOC_PATH)
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=10)
chunks = text_splitter.split_documents(data)

# store data into the vectorstore
if os.path.exists(CHROMA_PATH):
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=GPT4AllEmbeddings())
else:
    vectorstore = Chroma.from_documents(chunks, embedding=GPT4AllEmbeddings(), persist_directory=CHROMA_PATH)

retriever = vectorstore.as_retriever(search_kwargs={'k': 4})

ollama = Ollama(base_url='http://localhost:11434', model='llama2')
qa_chain = create_stuff_documents_chain(ollama, qa_prompt)
chain = create_retrieval_chain(retriever, qa_chain)
result = chain.invoke({'input': 'What is the main source of water in the United States?'})

print('\033[92m' + 'Input:' + '\033[0m', result['input'])
print('\033[92m' + 'Answer:' + '\033[0m', result['answer'])
print('\033[92m' + 'Context:' + '\033[0m', result['context'])