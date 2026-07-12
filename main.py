from fastapi import FastAPI,HTTPException
from database import TaskDatabase

app = FastAPI()
# 2. Turn the key to start the database machine
db = TaskDatabase()

@app.get("/")
def home():
    return {"message": "Welcome to TaskManager API."}

# 3. Create a route to get all tasks and create a new task using the methods from TaskDatabase
@app.get("/tasks")
def get_all_tasks():
    tasks = db.get_all_tasks()
    return {"tasks": tasks}

# 4. Create a route to create a new task using the methods from TaskDatabase
@app.post("/tasks",status_code=201)
def create_tasks(title: str, completed: bool = False):
    result = db.create_tasks(title, completed)
    return result 

# 5. Create a route to get a specific task by ID
@app.get("/tasks/{id}")
def get_task(id: int):
    result = db.get_tasks(id)
    if isinstance(result,dict) and "message" in result:
        raise HTTPException(status_code=404,detail=result['message'])
    return result

# 6. Create a route to update a specific task by ID
@app.put("/tasks/{id}")
def update_task(id: int, title: str = None, completed: bool = None):
    result = db.update_tasks(id, title, completed)
    if isinstance(result,dict) and "message" in result:
        raise HTTPException(status_code=404,detail=result['message'])
    return result

# 7. Create a route to delete a specific task by ID
@app.delete("/tasks/{id}")
def delete_task(id: int):
    result = db.delete_tasks(id)
    if isinstance(result,dict) and "message" in result:
        raise HTTPException(status_code=404,detail=result['message'])
    return result

    