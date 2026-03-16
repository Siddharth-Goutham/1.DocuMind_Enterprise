#Documinds Enterprise
# ---------------------------------------

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage, SystemMessage
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
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"token": os.getenv("HF_TOKEN")}
    )



''' Storing data in database using chrome.'''
vector_store = Chroma(
    collection_name= "documinds_collection",
    embedding_function=embeddings,
    persist_directory="chroma_langchain_db",  # Where to save data locally, remove if not necessary
)
vector_store.add_documents(texts)

#my part(Shamnad)

''' HuggingFace LLM '''
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token=os.getenv("HF_TOKEN"),
    temperature=0.3,
    max_new_tokens=512,
    task="text-generation",
    provider="featherless-ai",
)
chat_model = ChatHuggingFace(llm=llm)


def answer_question(user_question: str) -> str:

    # Step 1: Question → Vector → Fetch relevant chunks from ChromaDB
    relevant_docs = vector_store.similarity_search(user_question, k=4)

    if not relevant_docs:
        return "Sorry, I couldn't find relevant information in the document."

    # Step 2: Combine chunks as context
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Step 3: Pass context + question to HuggingFace LLM
    system_prompt = "You are a helpful assistant. Use the context below to answer the question.If the answer is not in the context, say \"I don't have enough information.\""
    user_prompt = f"Context:\n{context}\n\nQuestion: {user_question}"
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = chat_model.invoke(messages)
    return response.content


'''Run'''
if __name__ == "__main__":
    print("Documinds is ready! Ask anything about the document.")
    while True:
        question = input("Your question (or 'quit'): ").strip()
        if question.lower() == "quit":
            print("Goodbye!")
            break
        answer = answer_question(question)
        print("\nAnswer:\n", answer)



