#Documinds Enterprise
# ---------------------------------------
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from werkzeug.utils import secure_filename

''' Loading information from .env '''
load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

app = Flask(__name__)
app.config["SECRET_KEY"] = "SUPERSECRET"

'''Catching files uploaded from frontend'''
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "files")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")
    text_box = StringField("Ask anything...")
    ask_button = SubmitField("Ask")

''' Converting smaller chunks to vectors (numbers) using Hugging Face Embedding'''
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"token": os.getenv("HF_TOKEN")}
    )

''' HuggingFace LLM '''
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    huggingfacehub_api_token=os.getenv("HF_TOKEN"),
    temperature=0.3,
    max_new_tokens=512,
    task="text-generation"
)

chat_model = ChatHuggingFace(llm=llm)

@app.route("/", methods=["GET", "POST"])
def home():
    form = UploadFileForm()
    user_question = ""
    answer = ""

    '''Intitalizing vector database'''
    vector_store = Chroma(
        collection_name="documinds_collection",
        embedding_function=embeddings
    )

    # 1. Handle File Upload & Processing
    if form.validate_on_submit() and form.submit.data:
        '''Saving the pdf locally'''
        file = form.file.data
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            ''' Converting pdf to texts  '''
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            ''' Splitting huge texts in pdf to smaller chunks  '''
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
            texts = text_splitter.split_documents(docs)

            ''' Storing data in database using chrome.'''
            vector_store.add_documents(texts)

    if form.validate_on_submit() and form.ask_button.data:
        user_question = form.text_box.data
        '''Search through vector database'''
        relevant_docs = vector_store.similarity_search(user_question, k=4)
        if not relevant_docs:
            answer= "Sorry, I couldn't find relevant information in the document."
        else:
            '''Combine chunks as context'''
            context = "\n\n".join([doc.page_content for doc in relevant_docs])

            '''Pass context + question to HuggingFace LLM'''
            system_prompt = "You are a helpful assistant. Use the context below to answer the question.If the answer is not in the context, say \"I don't have enough information.\""
            user_prompt = f"Context:\n{context}\n\nQuestion: {user_question}"

            messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt)
                ]

            response = chat_model.invoke(messages)
            answer = response.content
    return render_template("index.html", form=form, question=user_question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)




