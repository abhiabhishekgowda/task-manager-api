from fastapi import FastAPI
# 1. Import your working class from database.py
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
@app.post("/tasks")
def create_tasks(title: str, completed: bool = False):
    result = db.create_tasks(title, completed)
    return result


