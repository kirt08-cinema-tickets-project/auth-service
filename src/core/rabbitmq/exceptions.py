import grpc

from src.core.grpc_server.exceptions import ServiceError


class ProblemsWithRMQException(ServiceError):
    grpc_status = grpc.StatusCode.UNAVAILABLE
    message = "RMQ Error"