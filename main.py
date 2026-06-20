from fastapi import FastAPI


app = FastAPI()

task_db = [
    {"id": 1, "title": "study fastapi", "complete": False},
    {"id": 2, "title": "solve leetcode", "complete": False}
]

@app.get("/")
def home():
    return {"message": "welcom to your task manager"}

@app.get("/tasks")
def view_all_tasks():
    return {"tasks": task_db}

@app.get("/task/{id}")
def view_task(id: int):

    # Check every task in the list
    for task in task_db:

        # Compare task id with URL id
        if task["id"] == id:

            # Return matching task
            return {"task": task}

    # If task not found
    return {"message": "Task not found"}

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