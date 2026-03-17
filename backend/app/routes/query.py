from fastapi import APIRouter, HTTPException
from app.models.schemas import QuestionRequest
from app.services.rag_service import generate_answer

router = APIRouter()

@router.post("/ask")
async def ask_question(req: QuestionRequest):
    try:
        answer = generate_answer(req.question, req.user_id)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
