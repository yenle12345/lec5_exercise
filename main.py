from fastapi import FastAPI, HTTPException, Query
from routers.todo_router import router as todo
from routers.auth import router as auth
from models.models import User, Todo
from database import Base, engine

app = FastAPI()

app.include_router(todo)
app.include_router(auth)
Base.metadata.create_all(bind = engine)



@app.get("/")
def home():
    return {"message": "HeLLO TO-DO API"}

@app.get("/health")
def health():
    return {"status":"ok"}








    