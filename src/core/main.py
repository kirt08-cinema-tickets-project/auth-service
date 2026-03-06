import os
import asyncio
import logging

from prometheus_client import start_http_server

from src.core.config import settings
from src.core.logger import setup_logging
from src.core.grpc_server.grpc_server import serve


mode = os.getenv("ENVIRONMENT", "development").lower()
if mode == "development":
    logging.basicConfig(
        format=settings.logger.format, 
        level=settings.logger.log_level   
    )
else:
    setup_logging()


if __name__ == "__main__":
    start_http_server(port = 9101)
    asyncio.run(serve())

