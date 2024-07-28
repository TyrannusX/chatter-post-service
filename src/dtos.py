import datetime
from pydantic import BaseModel

class CreatePostRequestDto(BaseModel):
    title: str
    description: str

class CreatePostResponseDto(BaseModel):
    id: str

class GetPostResponseDto(BaseModel):
    id: str
    author: str
    title: str
    description: str
    votes: int
    created_at: str
    created_by: str
    updated_at: str
    updated_by: str