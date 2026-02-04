import asyncio

from src.core.grpc_server.grpc_server import serve

if __name__ == "__main__":
    asyncio.run(serve())

