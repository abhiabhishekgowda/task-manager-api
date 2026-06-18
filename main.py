from fastapi import FastAPI


app = FastAPI()

task_db = [
    {"id": 1, "title": "study fastapi"},
    {"id": 2, "title": "solve leetcode"}
]

@app.get("/")
def home():
    return {"message": "welcom to your task manager"}

@app.get("/tasks")
def view_all_tasks():
    return {"tasks": task_db}

@app.get("/task/{id}")
def view_task(id: int):
    for task in task_db:
        if task["id"] == id:
            return {"task": task}
    return {"message": "task not found"}

@app.post("/task")
def create_task(id: int, title: str):
    task_db.append({"id": id, "title": title})
    return {"message": "task created successfully"}
    



