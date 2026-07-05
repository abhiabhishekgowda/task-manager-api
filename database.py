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
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
            """)
            conn.commit()
            print("Database successfully.")

