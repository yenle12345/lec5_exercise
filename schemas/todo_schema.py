from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Todo(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    is_done: bool = False
    created_at: datetime

class TodoUpdate(BaseModel):
    is_done: Optional[bool] = None
    title: Optional[str] = None
    description: Optional[str] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_done: bool
    created_at: datetime
    updated_at: datetime