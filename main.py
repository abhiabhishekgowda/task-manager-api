from fastapi import FastAPI, HTTPException
import sqlite3
from database import init_db, DB_NAME  # Import our config from database.py

app = FastAPI()

# Run the database setup immediately when the server boots up
init_db()

@app.get("/")
def home():
    return {"message": "Welcome to your SQLite Task Manager!"}

