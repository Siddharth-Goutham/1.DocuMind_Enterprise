#Documinds Enterprise
# ---------------------------------------

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv


''' Loading information from .env '''
load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")


''' Converting pdf to texts  '''
file_path= "policy.pdf"
loader=PyPDFLoader(file_path)

docs=loader.load()



''' Splitting huge texts in pdf to smaller chunks  '''
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = text_splitter.split_documents(docs)



''' Converting smaller chunks to vectors (numbers) using Hugging Face Embedding'''
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
    )



''' Storing data in database using chrome.'''
vector_store = Chroma(
    collection_name= "documinds_collection",
    embedding_function=embeddings,
    persist_directory="chroma_langchain_db",  # Where to save data locally, remove if not necessary
)
vector_store.add_documents(texts)


