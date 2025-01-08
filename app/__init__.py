from fastapi import FastAPI

from app.database import Base, engine
from app.endpoints import streams


def create_app():
    # Create database tables
    Base.metadata.create_all(bind=engine)

    app = FastAPI()

    # Include routes
    app.include_router(streams.router)

    return app
