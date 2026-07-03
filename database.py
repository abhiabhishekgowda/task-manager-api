import sqlite3

DB_NAME = "tasks.db"

class TaskDatabase:
    # 1. This function sets up the properties
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self.create_tables()  # 📢 This calls the method below!

    # 2. FIX: Shift this back to the left! It belongs to the Class, not __init__
    def create_tables(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL
            )
            """)
            conn.commit()
        print("📢 Database initialized and tasks table is ready!")

