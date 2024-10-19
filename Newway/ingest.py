from langchain.document_loaders import PyPDFLoader, PDFMinerLoader, DirectoryLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from os.path import join
import os
from constants import CHROMA_SETTINGS

for root,dir,files in os.walk("docs"):
        for file in files:
            if file.endswith(".pdf"):
                loader = PDFMinerLoader(join(root,file))
documents = loader.load()

textsplitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=500)
texts = textsplitter.split_documents(documents)


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(texts, embeddings, persist_directory="db", client_settings=CHROMA_SETTINGS)