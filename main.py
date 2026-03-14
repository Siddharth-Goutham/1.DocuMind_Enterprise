#Documinds Enterprise
# ---------------------------------------

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path= "policy.pdf"
loader=PyPDFLoader(file_path)

docs=loader.lazy_load()



text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = text_splitter.split_documents(docs)
