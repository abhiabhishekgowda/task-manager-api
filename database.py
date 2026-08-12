import sqlite3

class DatabaseConnection:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class TasksDatabase:
    def __init__(self, db_name="Tasks.db"):
        self.db_name = db_name
        self.create_table()
        self.create_user_table()

    def create_user_table(self):
        """Create users table if it doesn't exist."""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()

    def create_user(self, username: str, password: str):
        """Create a new user."""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            return {
                "id": cursor.lastrowid,
                "username": username
            }
    def create_table(self):
        """Create tasks table if it doesn't exist."""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.commit()
        
    def create_task(self, title: str, user_id: int, completed: bool = False):

        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO tasks (title, user_id, completed) VALUES (?, ?, ?)",
                (title, user_id, int(completed))
            )

            conn.commit()
            return{
                "id": cursor.lastrowid,
                "title": title,
                "user_id": user_id,
                "completed": completed
            }
    


    def get_all_tasks(self):
        """Fetch all tasks."""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            if not rows:
                return {"message": "No tasks exist yet."}
            return [
                {"id": row[0], "title": row[1], "completed": bool(row[2])}
                for row in rows
            ]

    def get_task(self, task_id: int):
        """Fetch a single task by ID."""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row is None:
                return {"message": f"No task found with id {task_id}"}
            return {"id": row[0], "title": row[1], "completed": bool(row[2])}

    def update_task(self, task_id: int, title: str = None, completed: bool = None):
        """Update task fields."""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row is None:
                return {"message": f"No task found with id {task_id}"}
            if title is not None:
                cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (title, task_id))
            if completed is not None:
                cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (int(completed), task_id))
            conn.commit()
            return {"id": row[0], "title": row[1], "completed": bool(row[2])}

    def delete_task(self, task_id: int):
        """Delete a task by ID."""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row is None:
                return {"message": f"No task found with id {task_id}"}
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return {"message": f"Task {task_id} deleted successfully."}

    def get_user(self, user_id: int):
        """Fetch a single user by ID."""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row is None:
                return {"message": f"No tasks found for user with id {user_id}"}
            return row
    def get_tasks_by_users(self,user_id: int):
        """Fetch all users."""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE user_id = ?",(user_id,))
            rows = cursor.fetchall()
            if not rows:
                return {"message": "No users exist yet."}
            return [{
                "id": row[0],
                "title": row[1],
                "completed": bool(row[2]),
                "user_id": row[2]
            }
            for row in rows]

            
db = TasksDatabase()
task = db.get_tasks_by_users(1)
print(task)
