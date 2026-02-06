import grpc

from src.core.grpc_server.exceptions import ServiceError


class IncorrectCodeException(ServiceError):
    grpc_status = grpc.StatusCode.NOT_FOUND
    message = "Incorrect code"

class CodeNotFoundException(ServiceError):
    grpc_status = grpc.StatusCode.NOT_FOUND
    message = "Code was not found"
