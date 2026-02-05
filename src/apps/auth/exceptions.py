import grpc

from src.core.grpc_server.exceptions import ServiceError


class TokenException(ServiceError):
    grpc_status = grpc.StatusCode.UNAUTHENTICATED