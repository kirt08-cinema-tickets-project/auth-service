import logging
import grpc

from kirt08_contracts.auth import auth_pb2_grpc
from kirt08_contracts.account import account_pb2_grpc

from src.core.config import settings
from src.core.container import init_objects
from src.core.prometheus import MetricsInterceptor
from src.core.grpc_server.auth import gRPC_Auth_Server
from src.core.grpc_server.account import gRPC_Account_Server


log = logging.getLogger(name = __name__)

async def serve():
    log.info("Server starting up...")
    
    otp, auth, account, telegram = await init_objects()

    server = grpc.aio.server(
        interceptors=[MetricsInterceptor()]
    )

    auth_pb2_grpc.add_AuthServiceServicer_to_server(
        gRPC_Auth_Server(auth, telegram),
        server
    )

    account_pb2_grpc.add_AccountServiceServicer_to_server(
        gRPC_Account_Server(account),
        server
    )
    url = f"{settings.grpc.server.host}:{settings.grpc.server.port}"
    log.info(url)
    server.add_insecure_port(url)
    await server.start()

    log.info("Server successfully started!")
    
    await server.wait_for_termination()