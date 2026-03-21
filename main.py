from fastapi import FastAPI, HTTPException, Query
from routers.todo_router import router as todo_router



app = FastAPI()

app.include_router(todo_router)
@app.get("/")
def home():
    return {"message": "HeLLO TO-DO API"}

@app.get("/health")
def health():
    return {"status":"ok"}







    