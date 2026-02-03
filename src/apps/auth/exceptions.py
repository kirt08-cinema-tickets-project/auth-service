import grpc

class ServiceError(Exception):
    grpc_status = grpc.StatusCode.INTERNAL

    def __init__(self, message: str = ""):
        super().__init__(message)
        self.message = message

class UserAlreadyExistsException(ServiceError):
    grpc_status = grpc.StatusCode.ALREADY_EXISTS

class TokenException(ServiceError):
    grpc_status = grpc.StatusCode.UNAUTHENTICATED