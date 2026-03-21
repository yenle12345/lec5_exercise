from schemas.todo_schema import Todo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories import todo_repository

def get_todos(db):
    return todo_repository.get_all(db)

def create_todo(db, todo: Todo):
    return todo_repository.create_todos(db, todo)

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