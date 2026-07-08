import sqlite3

class TaskDatabase:
    def __init__(self, db_name = "tasks.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
            """)
            conn.commit()
            print("Database successfully.")

    def create_tasks(self,title: str, completed: bool = False):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)",(title, completed))
            conn.commit()
            return {"message": "Tasks Create Successfully."}


    def get_all_tasks(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
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
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            rows = cursor.fetchone()
            if rows is None:
                return {"message": f"No tasks found with that ID: {id}"}
            return {
                "id": rows[0],
                "title": rows[1],
                "completed": bool(rows[2])
            }


    def update_tasks(self, id: int, title: str = None, completed: bool = None):
        with sqlite3.connect(self.db_name) as conn:
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
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            rows = cursor.fetchone()
            if rows is None:
                return {"message": f"No tasks found with that ID: {id}"}
            else:
                cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
                conn.commit()
                return {"message": "Tasks deleted successfully."}