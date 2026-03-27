from schemas.todo_schema import Todo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories import todo_repository
from datetime import datetime, date, time
from models.models import Todo as TodoModel

def get_todos(db):
    return todo_repository.get_all(db)

def create_todo_tags(db, todo: Todo, user_id):
    tags = []
    for tag_name in todo.tags:
        tag = todo_repository.get_tag_name(db, tag_name)
        if not tag:
            tag = todo_repository.create_tag(db, tag_name)
        tags.append(tag)
    
    new_todo = todo_repository.create_todos(db, todo.model_dump(exclude={"tags"}), user_id, tags)
    todo_repository.save(db)
    todo_repository.refresh(db, new_todo)

    return new_todo

def get_todo(db,todo_id: int):
    return todo_repository.get_by_id(db,todo_id)

def update_todo(db, todo_id: int, updated: Todo):
    return todo_repository.update_todo_id(db, todo_id, updated)

def delete_todo(db, todo_id: int):
    return todo_repository.delete_todo(db, todo_id)

def get_todos(db, is_done=None, q=None, sort=None, limit=10, offset=0):

    result = todo_repository.get_all(db)

    if is_done is not None:
        result = [t for t in result if t.is_done == is_done]

    if q:
        result = [t for t in result if q.lower() in t.title.lower()]

    if sort:
        reverse = False

        if sort.startswith("-"):
            reverse = True
            sort = sort[1:]

        if sort == "created_at":
            result = sorted(result, key=lambda x: x.created_at, reverse=reverse)

    total = len(result)

    result = result[offset: offset + limit]

    return {
        "items": result,
        "total": total,
        "limit": limit,
        "offset": offset
    }

def update_todo_service(db, todo_id, data):
    todo = todo_repository.get_by_id(db, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found") 

    return todo_repository.update(db, todo, data)


def complete_todo_service(db: Session, todo_id: int):
    todo = todo_repository.get_by_id(db, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo_repository.complete_todo(db, todo)


def get_overdue_todos(db: Session):
    now = datetime.now()
    return todo_repository.get_todos_by_filter(
        db, 
        filter_condition=(TodoModel.due_date < now) & (TodoModel.is_done == False)
    )

def get_today_todos(db: Session):
    # Logic: Lấy các task có due_date nằm trong ngày hôm nay (00:00:00 -> 23:59:59)
    today_start = datetime.combine(date.today(), time.min)
    today_end = datetime.combine(date.today(), time.max)
    
    return todo_repository.get_todos_by_filter(
        db,
        filter_condition=TodoModel.due_date.between(today_start, today_end)
    )