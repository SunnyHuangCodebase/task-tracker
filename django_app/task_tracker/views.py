from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import Task


def index(request: WSGIRequest):
    tasks = Task.objects.all()
    in_progress = [task for task in tasks if not task.complete]
    complete = [task for task in tasks if task.complete]
    return render(request, "django.html", {
        "in_progress": in_progress,
        "complete": complete
    })


@require_http_methods(["POST"])
def add(request: WSGIRequest):
    task_name = request.POST.get("name")
    Task(name=task_name)
    return redirect("index")


@require_http_methods(["PATCH"])
def update(request: WSGIRequest, task_id: int):
    Task.objects.get(id=task_id).toggle_complete()
    return redirect("index")


@require_http_methods(["DELETE"])
def delete(request: WSGIRequest, task_id: int):
    Task.objects.get(id=task_id).delete()
    return redirect("index")


@require_http_methods(["DELETE"])
def delete_all(request: WSGIRequest):
    Task.delete_all()
    return redirect("index")
