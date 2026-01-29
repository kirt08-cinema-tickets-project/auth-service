import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI


from src.core.config import settings
from src.core.db import db
from src.core.redis_db import get_redis_client

from src.apps.auth.router import router as auth_router
from src.apps.otp.router import router as otp_router

log = logging.getLogger(name = __name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level   
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting app")

    # POSTGRES
    log.info("Creating database tables")

    await db.create_tables()

    log.info("Database initialized successfully")

    # REDIS
    log.info("Connect to redis...")

    redis = get_redis_client()

    log.info("Successfully connected!")

    yield
    
    await redis.close()
    log.info("Shutting down app")

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(otp_router)

