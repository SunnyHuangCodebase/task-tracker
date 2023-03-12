from flask.testing import FlaskClient
from flask_wtf.csrf import generate_csrf

from server.database import Database
from server.model import Task


class TestRoutes:

    def test_get_homepage(self, client: FlaskClient):
        """Homepage returns Task App header without any tasks in initial view."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Task App" in response.data
        assert b"In Progress" not in response.data
        assert b"Completed" not in response.data

    def test_csrf_add_task(self, client: FlaskClient):
        """Adding a Task without CSRF token returns a Bad Request."""
        response = client.post("/add", data={"name": "Task 1"})
        assert response.status_code == 400

    def test_add_first_task(self, client: FlaskClient):
        """Adding a Task adds it to the homepage in the "In Progress" category."""
        before = client.get("/")
        assert b"In Progress" not in before.data
        assert b"Task 1" not in before.data
        assert b"Completed" not in before.data

        response = client.post("/add",
                               data={
                                   "name": "Task 1",
                                   "csrf_token": generate_csrf()
                               })
        assert response.status_code == 303

        after = client.get("/")
        assert b"In Progress" in after.data
        assert b"Task 1" in after.data
        assert b"Completed" not in after.data

    def test_csrf_toggle_complete_task(self, client: FlaskClient):
        """Toggling a Task without CSRF token returns a Bad Request."""
        response = client.patch("/update/1")
        assert response.status_code == 400

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

        response = client.patch(f"/update/{task_id}",
                                data={"csrf_token": generate_csrf()})
        assert response.status_code == 303

        after = client.get("/")
        assert b"In Progress" not in after.data
        assert b"Task 1" in after.data
        assert b"Completed" in after.data

        response = client.patch(f"/update/{task_id}",
                                data={"csrf_token": generate_csrf()})
        assert response.status_code == 303
        assert b"In Progress" in before.data
        assert b"Task 1" in before.data
        assert b"Completed" not in before.data

    def test_add_second_task(self, client: FlaskClient):
        """Adding another Task does not change any existing Tasks."""
        before = client.get("/")
        assert b"Task 1" in before.data
        assert b"Task 2" not in before.data

        response = client.post("/add",
                               data={
                                   "name": "Task 2",
                                   "csrf_token": generate_csrf()
                               })
        assert response.status_code == 303

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

        response = client.patch(f"/update/{task1}",
                                data={"csrf_token": generate_csrf()})
        assert response.status_code == 303

        update1 = client.get("/")
        assert b"In Progress" in update1.data
        assert b"Task 1" in update1.data
        assert b"Task 2" in update1.data
        assert b"Completed" in update1.data

        response = client.patch(f"/update/{task2}",
                                data={"csrf_token": generate_csrf()})
        assert response.status_code == 303

        update2 = client.get("/")
        assert b"In Progress" not in update2.data
        assert b"Task 1" in update2.data
        assert b"Task 2" in update2.data
        assert b"Completed" in update2.data

    def test_csrf_delete_task(self, client: FlaskClient):
        """Deleting a Task without CSRF token returns a Bad Request."""
        response = client.delete("/delete/1")
        assert response.status_code == 400

    def test_delete_task(self, client: FlaskClient, database: Database):
        """Deleting a Task does not change any other Tasks."""
        before = client.get("/")
        assert b"Task 1" in before.data
        assert b"Task 2" in before.data

        task1, _ = [task.id for task in Task.get_all(database)]

        response = client.delete(f"/delete/{task1}",
                                 data={"csrf_token": generate_csrf()})
        assert response.status_code == 303
        delete1 = client.get("/")
        assert b"Task 1" not in delete1.data
        assert b"Task 2" in delete1.data

    def test_csrf_delete_all_tasks(self, client: FlaskClient):
        """Deleting all Tasks without CSRF token returns a Bad Request."""
        response = client.delete("/delete_all")
        assert response.status_code == 400

    def test_delete_all_tasks(self, client: FlaskClient, database: Database):
        """Deleting all Tasks removes all Tasks and categories from the view"""
        Task("Task 1", database)

        before = client.get("/")
        assert b"Task 1" in before.data
        assert b"Task 2" in before.data
        assert b"In Progress" in before.data
        assert b"Completed" in before.data

        client.delete("/delete_all", data={"csrf_token": generate_csrf()})
        after = client.get("/")
        assert b"Task 1" not in after.data
        assert b"Task 2" not in after.data
        assert b"In Progress" not in after.data
        assert b"Completed" not in after.data
