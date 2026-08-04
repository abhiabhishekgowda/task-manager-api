import sqlite3

class TasksDatabase:
    def __init__(self, db_name="Tasks.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        """Create tasks table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.commit()

    def create_task(self, title: str, completed: bool = False):
        """Insert a new task."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO tasks (title, completed) VALUES (?, ?)",
                    (title, int(completed))
                )
                conn.commit()
                return {"message": "Task created successfully."}
        except sqlite3.Error as e:
            return {"error": str(e)}

    def get_all_tasks(self):
        """Fetch all tasks."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            if not rows:
                return {"message": "No tasks exist yet."}
            return [
                {"Id": row[0], "Title": row[1], "Completed": bool(row[2])}
                for row in rows
            ]

    def get_task(self, task_id: int):
        """Fetch a single task by ID."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row is None:
                return {"message": f"No task found with id {task_id}"}
            return {"Id": row[0], "Title": row[1], "Completed": bool(row[2])}

    def update_task(self, task_id: int, title: str = None, completed: bool = None):
        """Update task fields."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            if cursor.fetchone() is None:
                return {"message": f"No task found with id {task_id}"}

            if title is not None:
                cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (title, task_id))
            if completed is not None:
                cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (int(completed), task_id))
            conn.commit()
            return {"message": f"Task {task_id} updated successfully."}

    def delete_task(self, task_id: int):
        """Delete a task by ID."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            if cursor.fetchone() is None:
                return {"message": f"No task found with id {task_id}"}
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return {"message": f"Task {task_id} deleted successfully."}
