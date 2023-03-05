from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

from sqlalchemy import Boolean, Integer, Select, String, select
from sqlalchemy.orm import Mapped, mapped_column

from server.base import Model

if TYPE_CHECKING:
    from server.database import Database


class TaskNotFound(Exception):
    """Task doesn't exist in the database."""


class Task(Model):
    """A Task database object."""
    __tablename__: str = "task"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    complete: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String(100))

    def __init__(self, name: str, database: Database):
        self.name = name
        database.add(self)
        self.database = database

    @classmethod
    def get_all(cls, database: Database) -> Sequence[Task]:
        """Returns all tasks in the database."""
        return cls.query_all(database, select(Task))

    @classmethod
    def get_by_id(cls, database: Database, task_id: int) -> Task:
        """Returns a Task instance with the matching ID."""
        statement: Select[tuple[Task]] = select(Task).where(Task.id == task_id)

        task = cls.query(database, statement)

        if not task:
            raise TaskNotFound

        task.database = database
        return task

    def toggle_complete(self):
        """Toggles task's complete status between True and False."""
        self.complete = not self.complete
        self.database.commit()
