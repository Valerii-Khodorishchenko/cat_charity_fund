from fastapi import FastAPI

from app.core.config import settings
from app.api.routers import user_router


app = FastAPI(title=settings.app_title, description=settings.app_description)
app.include_router(user_router)
