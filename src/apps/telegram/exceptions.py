import grpc
from src.core.grpc_server.exceptions import ServiceError

class TelegramSignatureException(ServiceError):
    grpc_status = grpc.StatusCode.UNAUTHENTICATED,
    message = "Invalid Telegram Signature"

class SessionNotFoundException(ServiceError):
    grpc_status = grpc.StatusCode.NOT_FOUND
    message = "Session not found"

