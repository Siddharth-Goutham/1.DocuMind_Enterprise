from pydantic import BaseModel, field_validator, constr


class QuestionRequest(BaseModel):
    question: constr(min_length=3, max_length=1000)
    user_id: constr(min_length=3, max_length=100)

    @field_validator("question")
    @classmethod
    def clean_question(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Question cannot be empty or whitespace.")
        return v

    @field_validator("user_id")
    @classmethod
    def clean_user_id(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("User ID cannot be empty.")
        return v
