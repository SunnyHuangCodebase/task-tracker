from flask import Flask, redirect, render_template, request, url_for

from flask_app.server.database import Database
from flask_app.server.model import Task

app = Flask(
    __name__,
    root_path="flask_app",
)
DATABASE = Database()


@app.get("/")
def home():
    """Return all tasks."""
    tasks = Task.get_all(DATABASE)
    in_progress = [task for task in tasks if not task.complete]
    complete = [task for task in tasks if task.complete]

    return render_template("index.html",
                           in_progress=in_progress,
                           complete=complete)


@app.post("/add")
def add():
    task = Task(name=request.form.get("name"))
    DATABASE.add(task)
    return redirect(url_for("home"))


@app.get("/update/<int:task_id>")
def update(task_id: int):
    task = Task.get_by_id(DATABASE, task_id)
    task.toggle_complete(DATABASE)
    return redirect(url_for("home"))


@app.get("/delete/<int:task_id>")
def delete(task_id: int):
    task = Task.get_by_id(DATABASE, task_id)
    task.delete()
    return redirect(url_for("home"))


@app.get("/delete_all")
def delete_all():
    Task.delete_all(DATABASE)
    return redirect(url_for("home"))

