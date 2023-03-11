from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render

from .models import Task


class HttpResponseSeeOther(HttpResponseRedirect):
    status_code = 303


async def home(request: ASGIRequest):
    tasks = [task async for task in Task.objects.all()]
    in_progress = [task for task in tasks if not task.complete]
    complete = [task for task in tasks if task.complete]
    return render(request, "django.html", {
        "in_progress": in_progress,
        "complete": complete
    })


async def add(request: ASGIRequest):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    task_name = request.POST.get("name")
    await Task.a_create(task_name)
    return HttpResponseSeeOther("/")


async def update(request: ASGIRequest, task_id: int):
    if request.method != "PATCH":
        return HttpResponseNotAllowed(["PATCH"])

    await Task.a_toggle_complete(task_id)
    return HttpResponseSeeOther("/")


async def delete(request: ASGIRequest, task_id: int):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    await Task.a_delete(task_id)
    return HttpResponseSeeOther("/")


async def delete_all(request: ASGIRequest):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    await Task.a_delete_all()
    return HttpResponseSeeOther("/")
