📄 DocuMind – RAG-Based AI Chatbot

DocuMind is a Retrieval-Augmented Generation (RAG) based AI chatbot that allows users to upload PDF documents and ask questions about them. It combines document retrieval + language models to generate accurate, context-based answers.


🚀 Features
📂 Upload your own PDF documents
🔍 Extract and process document content
🧠 Semantic search using embeddings
💬 Ask questions in natural language
🤖 AI-generated answers based on document context
🌐 Web interface using Flask + HTML/CSS


🧠 How It Works (RAG Pipeline)
PDF Upload
   ↓
Document Loader (PyPDF)
   ↓
Text Splitting
   ↓
Embeddings (HuggingFace)
   ↓
Vector Database (Chroma)
   ↓
Retriever (Top-K Similar Chunks)
   ↓
LLM (HuggingFace)
   ↓
Answer


🛠️ Tech Stack
Backend
1. Python
2. Flask
3. Flask-WTF
   
AI / ML
1. LangChain
2. Hugging Face Transformers
3. Sentence Transformers
4. ChromaDB

Frontend
1. HTML
2. CSS
3. JavaScript


⚙️ Installation
1. Clone the Repository
git clone https://github.com/Siddharth-Goutham/1.DocuMind_Enterprise.git
cd 1.DocuMind_Enterprise

2. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Get the HF_Token from huggingface.co/settings/tokens.
Add the token in .env file


▶️ Run the Application
python app.py

Then open:
http://127.0.0.1:5000


💬 Usage
1. Upload a PDF file
2. Wait for processing
3. Ask questions related to the document
4. Get AI-generated answers

