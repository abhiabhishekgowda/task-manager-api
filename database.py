import sqlite3
import os                    
from dotenv import load_dotenv 

load_dotenv()

class DatabaseConnection:
    # 1. Let it handle its own defaults automatically without needing inputs passed in!
    def __init__(self, db_name: str = None):
        self.db_name = db_name or os.getenv("DATABASE_NAME", "tasks.db")
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

class TasksDatabase:
    # 2. Clean up this constructor so it doesn't need to manage db_name strings or pass them manually
    def __init__(self):
        self.create_table()

    def create_table(self):
        # 3. Call DatabaseConnection() cleanly without passing arguments!
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0
                )
            """)
            conn.commit()

    def create_tasks(self, title: str, completed: bool = False):
        with DatabaseConnection() as conn:  # 👈 Cleaned up here
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", (title, completed))
            conn.commit()
            return {"message": "Tasks Create Successfully."}

    def get_all_tasks(self):
        with DatabaseConnection() as conn:  # 👈 Cleaned up here
            cursor = conn.cursor()
            cursor.execute("SELECT * from tasks")
            tasks = cursor.fetchall()
            result = []
            for task in tasks:
                result.append({
                    "id": task[0],
                    "title": task[1],
                    "completed": bool(task[2])
                })
            return result
    
    def get_tasks(self, id: int):
        with DatabaseConnection() as conn:  # 👈 Cleaned up here
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row is None:
                return {"message": f"No Tasks found with that ID: {id}"}
            else:
                return {
                    "id": row[0],
                    "title": row[1],
                    "completed": bool(row[2])
                }

    def update_tasks(self, id: int, title: str = None, completed: bool = None):
        with DatabaseConnection() as conn:  # 👈 Cleaned up here
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            rows = cursor.fetchone()
            if rows is None:
                return {"message": f"No tasks found with that ID: {id}"}
            else:
                if title is not None:
                    cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (title, id))
                if completed is not None:
                    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, id))
                conn.commit()
                return {"message": "Tasks updated successfully."}

    def delete_tasks(self, id: int):
        with DatabaseConnection() as conn:  # 👈 Cleaned up here
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            rows = cursor.fetchone()
            if rows is None:
                return {"message": f"No tasks found with that ID: {id}"}
            else:
                cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
                conn.commit()
                return {"message": "Tasks deleted successfully."}