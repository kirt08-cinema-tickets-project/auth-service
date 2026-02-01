import grpc

class ServiceError(Exception):
    grpc_status = grpc.StatusCode.INTERNAL

    def __init__(self, message: str = ""):
        super().__init__(message)
        self.message = message

class ProblemsWithRedisException(ServiceError):
    grpc_status = grpc.StatusCode.UNAVAILABLE

class IncorrectCodeException(ServiceError):
    grpc_status = grpc.StatusCode.NOT_FOUND

class CodeNotFoundException(ServiceError):
    grpc_status = grpc.StatusCode.NOT_FOUND
