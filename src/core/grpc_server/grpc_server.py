import logging
import grpc

from kirt08_contracts.auth import auth_pb2_grpc
from kirt08_contracts.account import account_pb2_grpc

from src.core.config import settings
from src.core.container import init_objects
from src.core.grpc_server.auth import gRPC_Auth_Server
from src.core.grpc_server.account import gRPC_Account_Server


log = logging.getLogger(name = __name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level   
)

async def serve():
    # from src.core.db import db
    # await db.create_tables()
    # log.info("Drop Table")
    log.info("Server starting up...")

    
    otp, auth, account, telegram = await init_objects()

    server = grpc.aio.server()

    auth_pb2_grpc.add_AuthServiceServicer_to_server(
        gRPC_Auth_Server(auth, telegram),
        server
    )

    account_pb2_grpc.add_AccountServiceServicer_to_server(
        gRPC_Account_Server(account),
        server
    )

    server.add_insecure_port("localhost:50051")
    await server.start()

    log.info("Server successfully started!")
    
    await server.wait_for_termination()