# main.py
from fastapi import FastAPI, HTTPException
from schemas import TaskCreate, TaskResponse,TaskUpdate
from database import TasksDatabase

app = FastAPI()
db = TasksDatabase()

@app.get("/")
def home():
    return {"message": "Welcome to the Task Manager API"}

@app.post("/task",status_code=201)
def create_task(task: TaskCreate) -> TaskResponse:
    return db.create_task(task.title,task.completed)

@app.get("/task")
def view_all_task():
    return {"task": db.get_all_tasks()};

@app.get("/task/{task_id}")
def get_task(task_id: int):
    task = db.get_task(task_id)
    return task

@app.put("/task/{task_id}")
def update_task(task_id: int, task: TaskUpdate) -> TaskResponse:
    updated_task = db.update_task(task_id, task.title, task.completed)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    result = db.delete_task(task_id)
    return result


'''
# 1. CREATE TASK
@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate):
    return db.create_task(task.title, task.completed)

# 2. READ ALL TASKS
@app.get("/tasks/", response_model=list[TaskResponse])
def get_all_tasks():
    return db.get_all_tasks()

# 3. READ SINGLE TASK
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
'''