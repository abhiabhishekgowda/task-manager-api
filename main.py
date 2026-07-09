from fastapi import FastAPI, HTTPException, status
# 1. Import your working class from database.py
from database import TaskDatabase

app = FastAPI()
# 2. Turn the key to start the database machine
db = TaskDatabase()

@app.get("/")
def home():
    return {"message": "Welcome to TaskManager API."}

# 3. Create a route to get all tasks
@app.get("/tasks")
def get_all_tasks():
    tasks = db.get_all_tasks()
    return {"tasks": tasks}

# 4. Create a route to create a new task (Status 201 Created!)
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_tasks(title: str, completed: bool = False):
    result = db.create_tasks(title, completed)
    return result

# 5. Get a specific task by ID (With 404 safety trigger)
@app.get("/tasks/{id}")
def get_task(id: int):
    task = db.get_tasks(id)
    # If the database returned our custom error dictionary, raise a real 404!
    if isinstance(task, dict) and "message" in task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=task["message"]
        )
    return task

# 6. Update a specific task by ID (With 404 safety trigger)
@app.put("/tasks/{id}")
def update_task(id: int, title: str = None, completed: bool = None):
    result = db.update_tasks(id, title, completed)
    if "No tasks found" in result.get("message", ""):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=result["message"]
        )
    return result

# 7. Delete a specific task by ID (With 404 safety trigger)
@app.delete("/tasks/{id}")
def delete_task(id: int):
    result = db.delete_tasks(id)
    if "No tasks found" in result.get("message", ""):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=result["message"]
        )
    return result   

