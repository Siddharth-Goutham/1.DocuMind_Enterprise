import os
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.3,
    max_new_tokens=512,
    task="text-generation",
)

chat_model = ChatHuggingFace(llm=llm)


def generate_answer_from_context(context: str, question: str) -> str:
    system_prompt = (
        "You are a helpful assistant. Use the context below to answer the question. "
        "If the answer is not in the context, say 'I don't have enough information.'"
    )

    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = chat_model.invoke(messages)
    return response.content
