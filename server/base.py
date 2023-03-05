from __future__ import annotations

from typing import TYPE_CHECKING, Sequence, TypeVar

from sqlalchemy import Select, delete
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from server.database import Database

M = TypeVar("M", bound="Model")


class Model(DeclarativeBase):
    """The base ORM model."""
    database: Database

    @staticmethod
    def query(database: Database, statement: Select[tuple[M]]) -> M | None:
        """Returns a matching instance from the database or None."""
        instance = database.scalars(statement).first()
        return instance

    @staticmethod
    def query_all(database: Database,
                  statement: Select[tuple[M]]) -> Sequence[M]:
        """Returns list of matching instances from the database if any."""
        return database.scalars(statement).all()

    def delete(self):
        """Deletes instance from the database."""
        self.database.delete(self)
        self.database.commit()

    @classmethod
    def delete_all(cls, database: Database) -> None:
        """Deletes all class instances from the database."""
        statement = delete(cls)
        database.execute(statement)
        database.commit()
