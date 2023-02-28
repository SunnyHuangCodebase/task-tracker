import pytest
from sqlalchemy.exc import IntegrityError

from flask_app.server.database import Database
from flask_app.server.model import Task, TaskNotFound


class TestTask:

    @pytest.fixture(scope="session")
    def database(self) -> Database:
        return Database(url="sqlite:///testdb.sqlite")

    @pytest.fixture(scope="session")
    def task1(self, database: Database) -> Task:
        return Task("Task 1", database)

    def test_create_new_task(self, database: Database, task1: Task):
        task = Task.get_by_id(database, 1)
        assert task.id == task1.id
        assert task.name == task1.name
        assert task.complete == task1.complete == False

        with pytest.raises(TaskNotFound):
            assert Task.get_by_id(database, 2)

        new_task = Task("Task 2", database)
        task2 = Task.get_by_id(database, 2)
        assert task2.id == 2
        assert task2.name == new_task.name
        assert task2.complete is False

        assert Task.get_by_id(database, 1)
        assert new_task == task2

    def test_create_duplicate_task_id(self, database: Database):
        task = Task("Duplicate Task 1", database)
        with pytest.raises(IntegrityError):
            task.id = 1
            database.add(task)

    def test_read_task(self, database: Database, task1: Task):
        task = Task.get_by_id(database, 1)
        assert task.name == task1.name

    def test_update_task(self, database: Database):
        task1 = Task.get_by_id(database, 1)
        task2 = Task.get_by_id(database, 2)

        assert task1.complete is False
        assert task2.complete is False

        task1.toggle_complete()
        assert task1.complete is True
        assert task2.complete is False

        task1.toggle_complete()
        assert task1.complete is False
        assert task2.complete is False

    def test_delete_task(self, database: Database):
        task1 = Task.get_by_id(database, 1)
        task1.delete()
        with pytest.raises(TaskNotFound):
            assert Task.get_by_id(database, task1.id)
        assert Task.get_by_id(database, 2)

    def test_delete_tasks(self, database: Database):
        Task.delete_all(database)
        assert Task.get_all(database) == []
        with pytest.raises(TaskNotFound):
            assert Task.get_by_id(database, 1)
        with pytest.raises(TaskNotFound):
            assert Task.get_by_id(database, 2)
