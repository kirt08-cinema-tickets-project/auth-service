import logging
import grpc

from kirt08_contracts import auth_pb2, auth_pb2_grpc

from src.apps.otp.router import Otp
from src.core.redis_db import get_redis

from src.core.config import settings

log = logging.getLogger(name = __name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level   
)

class gRPC_Auth_Server:
    def __init__(self):
        self.service = auth_pb2_grpc.AuthServiceServicer

    async def SendOtp(self, request, context):
        """
        request.identifier 
        request.type       ["phone" | "email"]
        """

        response = auth_pb2.SendOtpResponse()
        redis = await get_redis()
        res = await Otp.send_otp(request.identifier, request.type, redis)
        
        if res:
            response.ok = True
        else:
            response.ok = False
        return response

async def serve():
    log.info("Server starting up...")

    server = grpc.aio.server()

    auth_pb2_grpc.add_AuthServiceServicer_to_server(
        gRPC_Auth_Server(),
        server
    )

    server.add_insecure_port("localhost:50051")
    await server.start()

    log.info("Server successfully started!")
    
    await server.wait_for_termination()