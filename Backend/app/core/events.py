from typing import Callable
from app.db.base_class import Base
from app.db.session import engine
from fastapi import FastAPI



def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        print("Starting app")
        # here you can add any startup code you need
        # for example, initializing a database connection
        # or loading a machine learning model
        # app.state.db = DatabaseConnection()
        # app.state.model = load_model()
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas correctamente")
    return start_app
