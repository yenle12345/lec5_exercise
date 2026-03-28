from fastapi import FastAPI, HTTPException, Query
from app.routers.todo_router import router as todo
from app.routers.auth import router as auth
from app.models.models import User, Todo
from app.database import Base, engine

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








    