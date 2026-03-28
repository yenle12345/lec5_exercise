from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, computed_field
from typing import Optional, List

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    is_done: bool = False
    due_date: Optional[datetime] = None
    tags: List[str] = []

class TodoUpdate(BaseModel):
    is_done: Optional[bool] = None
    title: Optional[str] = None
    description: Optional[str] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_done: bool
    created_at: datetime
    updated_at: datetime
    # Không khai báo trường 'tags' ở đây để tránh xung đột với property

    @computed_field
    @property
    def tag_list(self) -> List[str]:
        # Trả về tên tag nếu có, nếu không trả về list rỗng
        return [tag.name for tag in self.tags] if getattr(self, 'tags', None) else []
    
    model_config = ConfigDict(from_attributes=True)