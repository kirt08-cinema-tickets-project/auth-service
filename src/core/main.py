import asyncio

from src.core.config import settings
from src.core.grpc_server import serve

if __name__ == "__main__":
    asyncio.run(serve())

