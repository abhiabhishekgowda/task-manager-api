from fastapi import FastAPI, Request
from routers.tasks import router as tasks_router
from fastapi.responses import JSONResponse
from database import DatabaseError

app = FastAPI(title="Task Manager API", description="A simple API for managing tasks", version="1.0.0")

app.include_router(tasks_router)

@app.get("/")
def home():
    return {"message": "Welcome to the Task Manager API"}

@app.exception_handler(DatabaseError)
async def database_error_hanlder(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Database operation failed"}
    )