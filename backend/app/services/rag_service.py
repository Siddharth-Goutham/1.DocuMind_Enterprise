from app.services.vector_service import similarity_search
from app.services.qwen_service import generate_answer_from_context


def generate_answer(question: str, user_id: str):
    try:
        if not question or not question.strip():
            return "Question cannot be empty."

        if not user_id:
            return "User ID is required."

        docs = similarity_search(question, user_id)

        if not docs:
            return "No relevant information found."

        context_list = []
        for doc in docs:
            if hasattr(doc, "page_content") and doc.page_content:
                context_list.append(doc.page_content)

        if not context_list:
            return "Relevant documents found but content is empty."

        context = "\n\n".join(context_list[:5]) 

        answer = generate_answer_from_context(context, question)

        return answer or "Failed to generate answer."

    except Exception as e:
        print(f"[ERROR] generate_answer failed: {str(e)}")
        return "Something went wrong while generating the answer."
