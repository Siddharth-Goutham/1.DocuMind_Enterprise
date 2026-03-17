import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_PATH = os.getenv("DB_PATH", "backend/app/db/chroma_db")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

def get_vectorstore(user_id: str):
    return Chroma(
        collection_name=user_id,
        embedding_function=embedding,
        persist_directory=DB_PATH
    )

def add_documents(docs, user_id: str):
    db = get_vectorstore(user_id)
    db.add_documents(docs)
    db.persist()

def similarity_search(query: str, user_id: str):
    db = get_vectorstore(user_id)
    return db.similarity_search(query, k=4)
