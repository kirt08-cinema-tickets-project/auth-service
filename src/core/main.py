import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI


from src.core.config import settings
from src.core.db import db

from src.apps.router import router as auth_router

log = logging.getLogger(name = __name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level   
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting app")
    log.info("Creating database tables")

    await db.create_tables()

    log.info("Database initialized successfully")
    yield
    
    log.info("Shutting down app")

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)

