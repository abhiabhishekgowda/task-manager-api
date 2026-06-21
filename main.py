from fastapi import FastAPI


app = FastAPI()

task_db = [
    {"id": 1, "title": "study fastapi", "complete": False},
    {"id": 2, "title": "solve leetcode", "complete": False}
]

# 1) --------- VIEW HOME PAGE -------   
@app.get("/")
def home():
    return {"message": "welcom to your task manager"}

# 2) --------- VIEW ALL TAKS --------
@app.get("/tasks")
def view_all_tasks():
    return {"tasks": task_db}

# 3) --------- SEARCH TSAKS ---------
@app.get("/task/{id}")
def view_task(id: int):
    for task in task_db:
        if task["id"] == id:
            return {"task": task}
    return {"message": "Task not found"}

# 4) ---------- CRAETE TASK ---------
@app.post("/tasks")
def create_task(id: int, title: str):
    new_task = {
        "id": id,
        "title": title,
        "completed": False
    }
    task_db.append(new_task)
    return{
        "message": "Task added succeefully",
        "tasks": task_db
    }
# 5) ---------- UPDATE TASK ----------
@app.put("/tasks/{task_id}")
def update_task(task_id: int, completed: bool, title: str):
    for task in task_db:
        if task["id"] == task_id:
            task["completed"] = completed
            task["title"] = title
            return {
                "message": "Task updated successfully",
                "task": task
            }
    return {"message": "Task not found"}


# 6) ---------- DELETE TASK ---------- 

@app.delete("/task/{id}")
def delete_task(id: int):

    for task in task_db:
        if task["id"] == id:
            task_db.remove(task)
            return {
                "message": "Task deleted successfully",
                "tasks": task_db
            }
    return {"message": "Task not found"}
