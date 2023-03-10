import sys

from django_app.app import main as run_django
from fastapi_app.app import main as run_fastapi
from flask_app.app import main as run_flask

APPS = {
    "django": run_django,
    "fastapi": run_fastapi,
    "flask": run_flask,
    "1": run_django,
    "2": run_fastapi,
    "3": run_flask,
}

DEFAULT_APP = 1

def main(app_id: str):
    APPS[app_id]()


if __name__ == "__main__":
    app = sys.argv[-1] if sys.argv[-1] in APPS else str(DEFAULT_APP)
    main(app)
