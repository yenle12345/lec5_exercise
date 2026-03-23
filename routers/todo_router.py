from fastapi import APIRouter, HTTPException, Query, Depends
from schemas.todo_schema import Todo
from services import todo_service
from typing import Optional
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import todo_schema
from dependencies.auth import get_current_user
from database import get_db


router = APIRouter( prefix = '/api/v1/todos', tags = ['todos'])

@router.post("/todos")
def create_todo(todo: Todo, 
                db: Session = Depends(get_db),
                user = Depends(get_current_user)):
    return todo_service.create_todo(db, todo, user)

@router.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return todo_service.get_todos(db)

@router.get("/todos/{id}")
def get_todo(id: int,  db: Session = Depends(get_db)):
    todo = todo_service.get_todo(db, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/todos/{id}")
def update_todo(id: int, updated: Todo, db: Session = Depends(get_db)):
    todo = todo_service.update_todo(db, id, updated)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/todos/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = todo_service.delete_todo(db, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.get("/todos")
def get_todos(
    is_done: Optional[bool] = None,
    q: Optional[str] = None,
    sort: Optional[str] = None,
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    return todo_service.get_todos(db, is_done, q, sort, limit, offset)

@router.patch("/{id}", response_model = todo_schema.TodoResponse)
def update_todo(id: int, data: todo_schema.TodoUpdate, db: Session = Depends(get_db)):
    updated = todo_service.update_todo_service(
        db,
        id,
        data.model_dump(exclude_unset=True)
    )
    return updated

@router.post("/{id}/complete", response_model=todo_schema.TodoResponse)
def complete_todo(id: int, db: Session = Depends(get_db)):
    return todo_service.complete_todo_service(db, id)