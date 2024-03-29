import os

import uvicorn
from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from server.database import Database
from server.model import Task

templates = Jinja2Templates(directory="templates")


class FastAPIApp(FastAPI):
    database: Database

    def set_database(self, database: Database):
        """Sets a database to the FlaskApp."""
        self.database = database


SECRET_KEY = str(os.urandom(32))


class CSRFSettings(BaseModel):
    secret_key: str = SECRET_KEY
    csrf_header_name: str = "X-CSRF-TOKEN"


@CsrfProtect.load_config
def get_csrf_config():
    return CSRFSettings()


app = FastAPIApp()
app.set_database(Database())
app.mount("/static", StaticFiles(directory="./static"), name="static")


def get_db():
    yield app.database


@app.get("/")
async def home(request: Request,
               db: Database = Depends(get_db),
               csrf_protect: CsrfProtect = Depends()):
    tasks = Task.get_all(db)
    in_progress = [task for task in tasks if not task.complete]
    complete = [task for task in tasks if task.complete]
    csrf_token = csrf_protect.generate_csrf()
    return templates.TemplateResponse(
        "fastapi.html", {
            "request": request,
            "in_progress": in_progress,
            "complete": complete,
            "csrf_token": csrf_token
        })


@app.post("/add")
def add(request: Request,
        name: str = Form(...),
        db: Database = Depends(get_db),
        csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
    csrf_protect.validate_csrf(csrf_token)

    Task(name, db)

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.patch("/update/{task_id}")
def update(request: Request,
           task_id: int,
           db: Database = Depends(get_db),
           csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
    csrf_protect.validate_csrf(csrf_token)

    task = Task.get_by_id(db, task_id)
    task.toggle_complete()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.delete("/delete/{task_id}")
def delete(request: Request,
           task_id: int,
           db: Database = Depends(get_db),
           csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
    csrf_protect.validate_csrf(csrf_token)

    task = Task.get_by_id(db, task_id)
    task.delete()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.delete("/delete_all")
async def delete_all(request: Request, csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
    csrf_protect.validate_csrf(csrf_token)

    Task.delete_all(app.database)

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


def main():
    uvicorn.run(
        app,
        port=8000,
    )


if __name__ == "__main__":
    main()

# poetry add fastapi, uvicorn[standard], python-multipart, sqlalchemy, jinja2
