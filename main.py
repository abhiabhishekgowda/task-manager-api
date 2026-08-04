from fastapi import FastAPI
from database import TasksDatabase

app = FastAPI()
db = TasksDatabase()

@app.get("/")
def home():
    return {"message": "Welcome to Tasks Manager FastAPI"}

@app.get("/tasks")
def view_all_tasks():
    return {"tasks": db.get_all_tasks()}

@app.post("/tasks")
def create_task(title: str, completed: bool = False):
    return db.create_task(title, completed)

@app.get("/tasks/{task_id}")
def view_task(task_id: int):
    return db.get_task(task_id)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str = None, completed: bool = None):
    return db.update_task(task_id, title, completed)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return db.delete_task(task_id)
