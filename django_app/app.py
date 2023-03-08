import os
import sys
from pathlib import Path

import uvicorn
from django.core.asgi import get_asgi_application

path = Path(__file__).parent
sys.path.append(f"{path}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")


def main():
    app = get_asgi_application()
    uvicorn.run(
        app,
        port=8080,
    )


if __name__ == "__main__":
    main()
