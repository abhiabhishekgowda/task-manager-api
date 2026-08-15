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


class TaskDatabase:

    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0
                )
            """
            )
            conn.commit()

    def create_task(self, title: str, completed: bool = False):
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, completed) VALUES (?, ?)",
                (title, int(completed)),
            )
            conn.commit()
            return {
                "id": cursor.lastrowid,
                "title": title,
                "completed": completed,
            }

    def get_all_tasks(
        self,
        completed: bool | None = None,
        search: str | None = None,
        limit: int = 10,
        skip: int = 0,
        ):
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM tasks"
            conditions = []
            params = []

            # 1. Filter by completed status
            if completed is not None:
                conditions.append("completed = ?")
                params.append(int(completed))

            # 2. Filter by search keyword in title (case-insensitive search)
            if search:
                conditions.append("title LIKE ?")
                params.append(f"%{search}%")

            # Join conditions with WHERE if any exist
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            # 3. Add Pagination (LIMIT and OFFSET/SKIP)
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, skip])

            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [
                {"id": row[0], "title": row[1], "completed": bool(row[2])}
                for row in rows
            ]

    def get_task(self, task_id: int):
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return {"id": row[0], "title": row[1], "completed": bool(row[2])}


    def update_task(
        self, task_id: int, title: str = None, completed: bool = None
    ):
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row is None:
                return None  # Return None if not found

            if title is not None:
                cursor.execute(
                    "UPDATE tasks SET title = ? WHERE id = ?", (title, task_id)
                )
            if completed is not None:
                cursor.execute(
                    "UPDATE tasks SET completed = ? WHERE id = ?",
                    (int(completed), task_id),
                )

            conn.commit()

            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            updated_row = cursor.fetchone()
            return {
                "id": updated_row[0],
                "title": updated_row[1],
                "completed": bool(updated_row[2]),
            }

    def delete_task(self, task_id: int):
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row is None:
                return False  # Return False if row does not exist
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return True