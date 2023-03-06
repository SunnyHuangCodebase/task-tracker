from flask import Flask, redirect, render_template, request, url_for

from server.database import Database
from server.model import Task


class FlaskApp(Flask):
    database: Database

    def set_database(self, database: Database):
        """Sets a database to the FlaskApp."""
        self.database = database


app = FlaskApp(
    __name__,
    root_path="",
    template_folder="./templates",
    static_folder="./static",
)

app.set_database(Database())


@app.route("/", methods=["GET", "POST", "PATCH", "PUT", "DELETE"])
def home():
    """Return all tasks."""
    tasks = Task.get_all(app.database)
    in_progress = [task for task in tasks if not task.complete]
    complete = [task for task in tasks if task.complete]
    return render_template("flask.html",
                           in_progress=in_progress,
                           complete=complete)


@app.post("/add")
def add():
    task_name = request.form.get("name")
    Task(task_name, app.database)
    return redirect(url_for("home"))


@app.patch("/update/<int:task_id>")
def update(task_id: int):
    task = Task.get_by_id(app.database, task_id)
    task.toggle_complete()
    return redirect(url_for("home"))


@app.delete("/delete/<int:task_id>")
def delete(task_id: int):
    task = Task.get_by_id(app.database, task_id)
    task.delete()
    print("Deleted from Flask")
    return redirect(url_for("home"))


@app.delete("/delete_all")
def delete_all():
    Task.delete_all(app.database)
    return redirect(url_for("home"))


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
