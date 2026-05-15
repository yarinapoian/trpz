import mysql.connector
from typing import List, Optional, Dict, Any
from models import Task


class TaskService:
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        self.connect()

    def connect(self) -> bool:
        self.connection = mysql.connector.connect(**self.db_config)
        return self.connection.is_connected()

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def get_all_tasks(self) -> List[Task]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, title, status, created_at FROM tasks ORDER BY created_at DESC")

        tasks = []
        for row in cursor.fetchall():
            task = Task(
                id=row[0],
                title=row[1],
                status=row[2],
                created_at=row[3]
            )
            tasks.append(task)

        cursor.close()
        return tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, title, status, created_at FROM tasks WHERE id = %s", (task_id,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return Task(
                id=row[0],
                title=row[1],
                status=row[2],
                created_at=row[3]
            )
        return None

    def create_task(self, title: str) -> Optional[Task]:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, status) VALUES (%s, %s)",
            (title, "todo")
        )

        self.connection.commit()
        task_id = cursor.lastrowid
        cursor.close()

        return self.get_task_by_id(task_id)

    def mark_task_done(self, task_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE tasks SET status = %s WHERE id = %s",
            ("done", task_id)
        )

        self.connection.commit()
        success = cursor.rowcount > 0
        cursor.close()

        return success
