import grpc

from src.core.grpc_server.exceptions import ServiceError


class ProblemsWithRedisException(ServiceError):
    grpc_status = grpc.StatusCode.UNAVAILABLE
    message = "Redis Error"

class IncorrectCodeException(ServiceError):
    grpc_status = grpc.StatusCode.NOT_FOUND
    message = "Incorrect code"

class CodeNotFoundException(ServiceError):
    grpc_status = grpc.StatusCode.NOT_FOUND
    message = "Code was not found"
