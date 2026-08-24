from fastapi import FastAPI
from routers.tasks import router as tasks_router

app = FastAPI(title="Task Manager API", description="A simple API for managing tasks", version="1.0.0")

app.include_router(tasks_router)

@app.get("/")
def home():
    return {"message": "Welcome to the Task Manager API"}
