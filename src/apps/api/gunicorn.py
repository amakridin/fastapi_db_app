import os

from src.apps.api.app import Settings

settings = Settings()

bind = f"{settings.host}:{settings.port}"
worker_class = "uvicorn.workers.UvicornWorker"
wsgi_app = "src.apps.api.app:create_app()"
workers = os.cpu_count() * 2
