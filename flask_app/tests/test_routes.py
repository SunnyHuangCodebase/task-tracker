from flask.testing import FlaskClient

from flask_app.server.database import Database
from flask_app.server.model import Task


class TestRoutes:

    def test_get_homepage(self, client: FlaskClient):
        """Homepage returns Task App header without any tasks in initial view."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Task App" in response.data
        assert b"In Progress" not in response.data
        assert b"Completed" not in response.data

    def test_add_first_task(self, client: FlaskClient):
        """Adding a Task adds it to the homepage in the "In Progress" category."""
        before = client.get("/")
        assert b"In Progress" not in before.data
        assert b"Task 1" not in before.data
        assert b"Completed" not in before.data

        response = client.post("/add", data={"name": "Task 1"})
        assert response.status_code == 302

        after = client.get("/")
        assert b"In Progress" in after.data
        assert b"Task 1" in after.data
        assert b"Completed" not in after.data

    def test_toggle_complete_task(self, client: FlaskClient,
                                  database: Database):
        """List unfinished Tasks under "In Progress" and finished Tasks under "Completed"."""
        before = client.get("/")
        assert b"In Progress" in before.data
        assert b"Task 1" in before.data
        assert b"Completed" not in before.data

        task_id = [
            task.id for task in Task.get_all(database) if task.name == "Task 1"
        ][0]

        response = client.patch(f"/update/{task_id}")
        assert response.status_code == 302

        after = client.get("/")
        assert b"In Progress" not in after.data
        assert b"Task 1" in after.data
        assert b"Completed" in after.data

        response = client.patch(f"/update/{task_id}")
        assert response.status_code == 302
        assert b"In Progress" in before.data
        assert b"Task 1" in before.data
        assert b"Completed" not in before.data

    def test_add_second_task(self, client: FlaskClient):
        """Adding another Task does not change any existing Tasks."""
        before = client.get("/")
        assert b"Task 1" in before.data
        assert b"Task 2" not in before.data

        response = client.post("/add", data={"name": "Task 2"})
        assert response.status_code == 302

        after = client.get("/")
        assert b"Task 1" in after.data
        assert b"Task 2" in after.data

    def test_toggle_complete_multiple_tasks(self, client: FlaskClient,
                                            database: Database):
        """"In Progress" and "Completed" sections only show if Tasks are listed under them."""
        before = client.get("/")
        assert b"In Progress" in before.data
        assert b"Task 1" in before.data
        assert b"Task 2" in before.data
        assert b"Completed" not in before.data

        task1, task2 = [task.id for task in Task.get_all(database)]

        response = client.patch(f"/update/{task1}")
        assert response.status_code == 302

        update1 = client.get("/")
        assert b"In Progress" in update1.data
        assert b"Task 1" in update1.data
        assert b"Task 2" in update1.data
        assert b"Completed" in update1.data

        response = client.patch(f"/update/{task2}")
        assert response.status_code == 302

        update2 = client.get("/")
        assert b"In Progress" not in update2.data
        assert b"Task 1" in update2.data
        assert b"Task 2" in update2.data
        assert b"Completed" in update2.data

    def test_delete_task(self, client: FlaskClient, database: Database):
        """Deleting a Task does not change any other Tasks."""
        before = client.get("/")
        assert b"Task 1" in before.data
        assert b"Task 2" in before.data

        task1, _ = [task.id for task in Task.get_all(database)]

        client.delete(f"/delete/{task1}")
        delete1 = client.get("/")
        assert b"Task 1" not in delete1.data
        assert b"Task 2" in delete1.data

    def test_delete_all_tasks(self, client: FlaskClient, database: Database):
        """Deleting all Tasks removes all Tasks and categories from the view"""
        Task("Task 1", database)

        before = client.get("/")
        assert b"Task 1" in before.data
        assert b"Task 2" in before.data
        assert b"In Progress" in before.data
        assert b"Completed" in before.data

        client.delete("/delete_all")
        after = client.get("/")
        assert b"Task 1" not in after.data
        assert b"Task 2" not in after.data
        assert b"In Progress" not in after.data
        assert b"Completed" not in after.data
