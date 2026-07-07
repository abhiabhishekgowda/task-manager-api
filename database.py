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
            return tasks