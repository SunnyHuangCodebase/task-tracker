import pytest
from sqlalchemy.exc import IntegrityError

from server.database import Database
from server.model import Task, TaskNotFound


class TestTask:

    def test_create_new_task(self, database: Database, task1: Task):
        """New tasks are added correctly in the database."""
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
        """Task with non-unique ID cannot be added to the database."""
        task = Task("Duplicate Task 1", database)
        with pytest.raises(IntegrityError):
            task.id = 1
            database.add(task)

    def test_read_task(self, database: Database, task1: Task):
        """Task read operations on the database return the selected task with correct attributes."""
        task = Task.get_by_id(database, 1)
        assert task.name == task1.name

    def test_update_task(self, database: Database):
        """Task update operations toggle the complete status of the selected task only."""
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
        """Task delete operations only remove the selected task from the database."""
        task1 = Task.get_by_id(database, 1)
        task1.delete()
        with pytest.raises(TaskNotFound):
            assert Task.get_by_id(database, task1.id)
        assert Task.get_by_id(database, 2)

    def test_delete_all_tasks(self, database: Database):
        """Task delete all operations removes every Task from the database."""
        Task("Task 1", database)
        Task("Task 2", database)
        Task("Task 3", database)
        assert len(Task.get_all(database)) > 0

        Task.delete_all(database)

        assert Task.get_all(database) == []
        with pytest.raises(TaskNotFound):
            assert Task.get_by_id(database, 1)
        with pytest.raises(TaskNotFound):
            assert Task.get_by_id(database, 2)
