import uvicorn

from src.apps.api.app import Settings, create_app

if __name__ == "__main__":
    settings = Settings()
    uvicorn.run(
        create_app(settings), host="0.0.0.0", port=settings.port, log_config=None
    )
