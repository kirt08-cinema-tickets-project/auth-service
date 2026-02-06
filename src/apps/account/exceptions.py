import grpc

from src.core.grpc_server.exceptions import ServiceError


class EmailAlreadyInUseException(ServiceError):
    grpc_status = grpc.StatusCode.ALREADY_EXISTS,
    message = "Email already in use"

class PendingNotFoundException(ServiceError):
    grpc_status = grpc.StatusCode.NOT_FOUND,
    message = "Pending was not found"

class IncorrectEmailException(ServiceError):
    grpc_status = grpc.StatusCode.INVALID_ARGUMENT,
    message = "Email mismatch"

class PhoneAlreadyInUseException(ServiceError):
    grpc_status = grpc.StatusCode.ALREADY_EXISTS,
    message = "Phone already in use"

class PendingNotFoundException(ServiceError):
    grpc_status = grpc.StatusCode.NOT_FOUND,
    message = "Pending was not found"

class IncorrectPhoneException(ServiceError):
    grpc_status = grpc.StatusCode.INVALID_ARGUMENT,
    message = "Phone mismatch"