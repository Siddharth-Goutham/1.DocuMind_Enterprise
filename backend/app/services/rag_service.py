from app.services.vector_service import similarity_search
from app.services.qwen_service import generate_answer_from_context

def generate_answer(question: str, user_id: str):
    docs = similarity_search(question, user_id)

    if not docs:
        return "No relevant information found."

    context = "\n\n".join([doc.page_content for doc in docs])

    return generate_answer_from_context(context, question)
