from app.api.routes.api import router as api_router
from app.core.config import (
    API_PREFIX,
    DEBUG,
    MEMOIZATION_FLAG,
    PROJECT_NAME,
    VERSION,
    CORS_ORIGINS,
)
from app.core.events import create_start_app_handler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    # CORS for frontend dev and configured origins
    application.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_router, prefix=API_PREFIX)
    application.add_event_handler("startup", create_start_app_handler(application))
    return application

app = get_application()
