# Request and Response models

from pydantic import BaseModel


class MCQRequest(BaseModel):
    # When user wants to generate MCQs
    text: str  # The text to make questions from
    num_questions: int = 5  # How many questions they want


class MCQResponse(BaseModel):
    # What we send back to user
    questions: list  # List of all questions
    status: str  # success or error
