from typing import  List

from sqlalchemy.orm import Session, joinedload
from app.models.models import Todo as TodoModel
from app.models.models import Tag
from datetime import date, date, time

def get_all(db: Session):
    return db.query(TodoModel).all()

def create_todos(db: Session,todo, user_id, tags: list):
    new_todo = TodoModel(**todo, owner_id = user_id, tags = tags)
    db.add(new_todo)
    
    return new_todo

def get_by_id(db: Session, todo_id: int):
    return db.query(TodoModel)\
        .options(joinedload(TodoModel.tags))\
        .filter(TodoModel.id == todo_id)\
        .first()



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

def create_tag(db, name: str):
    tag = Tag(name = name)
    db.add(tag)
    return tag

def get_tag_name(db, name: str):
    return db.query(Tag).filter(Tag.name == name).first()

def save(db):
    db.commit()

def refresh(db: Session, obj):
    db.refresh(obj)


def get_todos_by_filter(db: Session, filter_condition):
    return db.query(TodoModel)\
        .options(joinedload(TodoModel.tags))\
        .filter(filter_condition)\
        .all()