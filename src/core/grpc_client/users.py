import grpc

from kirt08_contracts.users import users_pb2, users_pb2_grpc

from src.core.config import settings


class UsersClient:
    def __init__(self):
        self._channel = grpc.aio.insecure_channel(
            f"{settings.grpc.client.host}:{settings.grpc.client.port}"
        )
        self._stub = users_pb2_grpc.UsersServiceStub(self._channel)

    async def get_me(self, id: str):
        request = users_pb2.GetMeRequest(
            id = id
        )
        response = await self._stub.GetMe(request)
        return response