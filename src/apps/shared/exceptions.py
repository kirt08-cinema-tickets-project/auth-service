import grpc

from src.core.grpc_server.exceptions import ServiceError

class UserAlreadyExistsException(ServiceError):
    grpc_status = grpc.StatusCode.ALREADY_EXISTS
    message = "User already exists"

class ProblemsWithRedisException(ServiceError):
    grpc_status = grpc.StatusCode.UNAVAILABLE
    message = "Redis Error"