from fastapi import FastAPI

from app.database import Base, engine
from app.endpoints import destination_route, stream_route


def create_app():
    # Create database tables
    Base.metadata.create_all(bind=engine)

    app = FastAPI()

    # Include routes
    app.include_router(stream_route.router)
    app.include_router(destination_route.router)

    return app
