from django_app.app import main as run_django
from fastapi_app.app import main as run_fastapi
from flask_app.app import main as run_flask

app = {
    1: run_flask,
    2: run_fastapi,
    3: run_django
}

def main(app_id: int):
    app[app_id]()


if __name__ == "__main__":
    APP_ID = 3
    main(APP_ID)
