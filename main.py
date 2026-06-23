from fastapi import FastAPI, HTTPException
from typing import Optional
import json
import os

app = FastAPI()

FILE_PATH = "tasks.json"

# Helper Function 1: Load data from the hard drive JSON file
def load_tasks():
    if not os.path.exists(FILE_PATH):
        return []  # Return empty list if file doesn't exist yet
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []  # Return empty list if file gets corrupted

# Helper Function 2: Save data onto the hard drive JSON file
def save_tasks(tasks):
    with open(FILE_PATH, "w") as file:
        json.dump(tasks, file, indent=4)

# 1) VIEW HOME PAGE
@app.get("/")
def home():
    return {"message": "Welcome to your permanent JSON task manager!"}

# 2) VIEW ALL TASKS
@app.get("/tasks")
def view_all_tasks():
    tasks_db = load_tasks()
    return {"tasks": tasks_db}

# 3) SEARCH SINGLE TASK
@app.get("/tasks/{id}")
def view_task(id: int):
    tasks_db = load_tasks()
    for task in tasks_db:
        if task["id"] == id:
            return {"task": task}
    raise HTTPException(status_code=404, detail="Task not found")

# 4) CREATE NEW TASK (With ID Duplicate Prevention Check!)
@app.post("/tasks")
def create_task(id: int, title: str):
    tasks_db = load_tasks()
    
    # Block duplicate IDs at the door
    for task in tasks_db:
        if task["id"] == id:
            raise HTTPException(status_code=400, detail="This Task ID already exists!")
            
    new_task = {
        "id": id,
        "title": title,
        "completed": False
    }
    tasks_db.append(new_task)
    save_tasks(tasks_db)  # Permanent save!
    return {"message": "Task added successfully", "tasks": tasks_db}

# 5) UPDATE TASK (Smart Partial Updates!)
@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: Optional[str] = None, completed: Optional[bool] = None):
    tasks_db = load_tasks()
    for task in tasks_db:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if completed is not None:
                task["completed"] = completed
                
            save_tasks(tasks_db)  # Permanent save!
            return {"message": "Task updated successfully", "task": task}
            
    raise HTTPException(status_code=404, detail="Task not found")

# 6) DELETE TASK
@app.delete("/tasks/{id}")
def delete_task(id: int):
    tasks_db = load_tasks()
    for task in tasks_db:
        if task["id"] == id:
            tasks_db.remove(task)
            save_tasks(tasks_db)  # Permanent save!
            return {"message": "Task deleted successfully", "tasks": tasks_db}
            
    raise HTTPException(status_code=404, detail="Task not found")