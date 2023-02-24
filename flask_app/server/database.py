from __future__ import annotations

from psycopg2.errors import UniqueViolation
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from flask_app.server.base import Model


class Database(Session):
    """A Database session that contains a collection of database objects and
    enables transactions.

    Attributes:
        url: A string of the database's connection URL.
        engine: The database Engine.
    """
    engine: Engine

    def __init__(self,
                 url: str = "sqlite:///db.sqlite",
                 echo: bool = False) -> None:
        self.engine = create_engine(url, echo=echo)
        Model.metadata.create_all(self.engine)
        super().__init__(self.engine, expire_on_commit=False)

    def commit(self):
        """Commits or rolls back changes if commit fails."""
        try:
            super().commit()
        except (IntegrityError, UniqueViolation):
            self.rollback()
            self.commit()
            raise

    def add(self, instance: object, _warn: bool = True) -> None:
        """Adds instance to the database."""
        super().add(instance, _warn)
        self.commit()

    def delete(self, instance: object) -> None:
        """Deletes instance to the database."""
        super().delete(instance)
        self.commit()
