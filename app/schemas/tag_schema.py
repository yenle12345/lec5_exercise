from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TagBase(BaseModel):
    name: str

class TodoCreate(BaseModel):
    title: str
    due_date: Optional[datetime] = None
    tags: List[str] = []