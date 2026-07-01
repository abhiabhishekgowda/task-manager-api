import sqlite3

DB_NAME = "tasks.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Create our single table with proper SQLite types
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL
        )
        """)
        
        conn.commit()
    print("📢 Database initialized and tasks table is ready!")

init_db ()