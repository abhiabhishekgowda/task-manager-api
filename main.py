from fastapi import FastAPI, HTTPException,Query
from database import TaskDatabase
from schemas import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI()
db = TaskDatabase()

@app.get("/")
def home():
    return {"message": "Welcome To Task Manager API."}

@app.get("/tasks")
def get_all_tasks(completed: bool | None = None, search: str | None = None, limit: int = Query(10, ge=2), skip: int = Query(0, ge=0))-> list[TaskResponse]:
    tasks = db.get_all_tasks(completed, search, limit, skip)
    return tasks

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate)-> TaskResponse:
    return db.create_task(task.title, task.completed)

@app.get("/tasks/{task_id}")
def get_task(task_id: int)-> TaskResponse:
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found {task_id}")
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate)-> TaskResponse:
    new_task = db.update_task(task_id, task.title, task.completed)
    if new_task is None:
        raise HTTPException(status_code=404, detail=f"Task not found {task_id}")
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = db.delete_task(task_id)
    if deleted is False:
        raise HTTPException(status_code=404, detail=f"Task not found {task_id}")
    return {"message": f"Task {task_id} deleted successfully."}