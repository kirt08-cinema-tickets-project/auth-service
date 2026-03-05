import asyncio

from prometheus_client import start_http_server

from src.core.grpc_server.grpc_server import serve


if __name__ == "__main__":
    start_http_server(port = 9101)
    asyncio.run(serve())

