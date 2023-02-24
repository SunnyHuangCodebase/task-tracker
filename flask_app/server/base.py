from __future__ import annotations

from typing import TYPE_CHECKING, Self, Sequence, TypeVar

from sqlalchemy import Select, delete
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from flask_app.server.database import Database

M = TypeVar("M", bound="Model")


class Model(DeclarativeBase):
    """The base ORM model."""
    database: Database

    @staticmethod
    def query(database: Database,
              statement: Select[tuple[Self]]) -> Self | None:
        """Returns a matching instance from the database or None."""
        instance = database.scalars(statement).first()

        if instance:
            instance.database = database

        return instance

    @staticmethod
    def query_all(database: Database,
                  statement: Select[tuple[Self]]) -> Sequence[Self]:
        """Returns list of matching instances from the database if any."""
        return database.scalars(statement).all()

    def add(self, instance: Model):
        """Adds instance to the database."""
        self.database.add(instance)

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
