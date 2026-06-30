from fastapi import FastAPI, HTTPException
from typing import Optional
import sqlite3

app = FastAPI()
DB_NAME = "tasks.db"

app = FastAPI()

def create_database():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
        """)
        conn.commit()


@app.get("/")
def home():
    return{"message": "Welcome to tasks manager api"}

@app.get("/tasks")
def view_all_tasks():
    tasks_db = load_data()
    return {"Tasks": tasks_db}

@app.get("/tasks/{id}")
def view_tasks(id: int):
    tasks_db = load_data()
    for tasks in tasks_db:
        if tasks['id'] == id:
            return {"tasks": tasks}
    raise HTTPException(status_code=404,detail="No tasks found!")

@app.post("/tasks")
def create_tasks(id: int,title: str):
    tasks_db = load_data()
    for tasks in tasks_db:
        if tasks['id'] == id:
            raise HTTPException(status_code=404,detail="The ID alredy exists")
    new_tasks = {
        "id": id,
        "title": title,
        "completed": False
    }
    tasks_db.append(new_tasks)
    save_data(tasks_db)
    return {"message": "Task added successfully", "tasks": tasks_db}

@app.put("/tasks/{tasks_id}")
def update_tasks(tasks_id: int, title: Optional[str], completed: Optional[bool]):
    tasks_db = load_data()
    for tasks in tasks_db:
        if tasks['id'] == tasks_db:
            if title is not None:
                tasks['title'] = title
            if completed is not None:
                tasks["completed"] = completed
            save_tasks(tasks_db)  # Permanent save!
            return {"message": "Task updated successfully", "task": task}
            
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}")
def delete_tasks(id: int):
    tasks_db = load_data()
    for tasks in tasks_db:
        if tasks['id'] == id:
            tasks_db.reverse(tasks)
            save_tasks(tasks_db)  # Permanent save!
        return {"message": "Task deleted successfully", "task": task}
            
    raise HTTPException(status_code=404, detail="Task not found!")