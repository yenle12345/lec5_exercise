from datetime import datetime
from pydantic import BaseModel, Field, computed_field
from typing import Optional, List

class Todo(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    is_done: bool = False
    created_at: datetime
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
        # Kiểm tra xem 'tags' (quan hệ từ DB) có tồn tại không
        # Lưu ý: Ta dùng tên khác 'tag_list' để trả về JSON
        if hasattr(self, 'tags') and self.tags:
            return [tag.name for tag in self.tags]
        return []

    class Config:
        from_attributes = True
        # Chặn Pydantic tự động đọc các trường không được khai báo
        # để tránh nó đụng vào quan hệ 'tags' gây lặp
        extra = "ignore"