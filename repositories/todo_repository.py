from typing import  List

from sqlalchemy.orm import Session
from models.models import Todo as TodoModel


def get_all(db: Session):
    return db.query(TodoModel).all()

def create_todos(db: Session,todo, user_id):
    new_todo = TodoModel(**todo.model_dump(), owner_id = user_id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo

def get_by_id(db: Session, todo_id: int):
    return db.query(TodoModel).filter(TodoModel.id == todo_id).first()



def update_todo_id(db: Session, id: int, updated):
    todo = db.query(TodoModel).filter(TodoModel.id == id).first()

    if not todo:
        return None

    for key, value in updated.model_dump().items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)

    return todo


def delete_todo(db: Session, id: int):
    todo = db.query(TodoModel).filter(TodoModel.id == id).first()
    if not todo:
        return None
    db.delete(todo)
    db.commit()

    return todo

def update(db, todo, data):
    for key, value in data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)

    return todo  


def complete_todo(db: Session, todo):
    if not todo:
        return None

    todo.completed = True

    db.commit()
    db.refresh(todo)

    return todo

