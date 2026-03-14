#Documinds Enterprise
# ---------------------------------------

from langchain_community.document_loaders import PyPDFLoader

file_path= "policy.pdf"
loader=PyPDFLoader(file_path)

docs=loader.lazy_load()
for document in docs:
    print(document)
