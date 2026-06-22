from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# 1) OUR INITIAL DATABASE (Fixed the "complete" typo to "completed"!)
task_db = [
    {"id": 1, "title": "study fastapi", "completed": False},
    {"id": 2, "title": "solve leetcode", "completed": False}
]

# 2) VIEW HOME PAGE
@app.get("/")
def home():
    return {"message": "Welcome to your task manager!"}

# 3) VIEW ALL TASKS (Unified path: GET /tasks)
@app.get("/tasks")
def view_all_tasks():
    return {"tasks": task_db}

# 4) SEARCH SINGLE TASK (Unified path layout: GET /tasks/{id})
@app.get("/tasks/{id}")
def view_task(id: int):
    for task in task_db:
        if task["id"] == id:
            return {"task": task}
    return {"message": "Task not found"}

# 5) CREATE NEW TASK (Unified path layout: POST /tasks)
@app.post("/tasks")
def create_task(id: int, title: str):
    for task in task_db:
        if task["id"] == id:
            return {"message": "Task with this ID already exists!"}
    new_task = {"id": id, "title": title, "completed": False}
    task_db.append(new_task)
    return {"message": "Task created successfully", "task": new_task}
    

# 6) UPDATE TASK (Smart Partial Updates!)
@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: Optional[str] = None, completed: Optional[bool] = None):
    for task in task_db:
        if task["id"] == task_id:
            # If the user provided a new title, change it. Otherwise, keep the old one!
            if title is not None:
                task["title"] = title
            
            # If the user provided a new status, change it. Otherwise, keep the old one!
            if completed is not None:
                task["completed"] = completed
                
            return {"message": "Task updated successfully", "task": task}
            
    return {"message": "Task not found"}

# 7) DELETE TASK (Unified path layout: DELETE /tasks/{id})
@app.delete("/tasks/{id}")
def delete_task(id: int):
    for task in task_db:
        if task["id"] == id:
            task_db.remove(task)
            return {"message": "Task deleted successfully", "tasks": task_db}
    return {"message": "Task not found"}

