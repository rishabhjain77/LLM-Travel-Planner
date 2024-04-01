import ollama
import bs4
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import chromadb

import os
documents = []

# Iterate through each file path
directory_path = "./data"

# Iterate through files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        # Construct the file path
        file_path = os.path.join(directory_path, filename)
        #print(file_path)
        # Use the TextLoader to load the text content from the file
        loader = TextLoader(file_path)
        loaded_documents = loader.load()
        # Extract the page content from each loaded document
        for document in loaded_documents:
            page_content = document.page_content
            documents.append(page_content)

docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Create Ollama embeddings and vector store
embeddings = OllamaEmbeddings(model="llama2")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

# Create the retriever
retriever = vectorstore.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Define the Ollama LLM function
def ollama_llm(prompt, context):
    formatted_prompt = f"Question: {prompt}\n\nContext: {context}"
    response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']

# Define the RAG chain
def rag_chain(question):
    retrieved_docs = retriever.invoke(question)
    formatted_context = format_docs(retrieved_docs)
    return ollama_llm(question, formatted_context)

