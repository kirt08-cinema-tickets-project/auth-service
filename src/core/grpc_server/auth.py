import grpc
from kirt08_contracts.auth import auth_pb2, auth_pb2_grpc

from src.apps.auth import Auth
from src.apps.auth.exceptions import (
    UserAlreadyExistsException,
    TokenException,
)


from src.apps.otp.exceptions import (
    ProblemsWithRedisException,
    IncorrectCodeException,
    CodeNotFoundException,
)


class gRPC_Auth_Server:
    def __init__(self):
        self.service = auth_pb2_grpc.AuthServiceServicer

    async def SendOtp(self, request, context):
        """
        request.identifier 
        request.type       ["phone" | "email"]
        """

        response = auth_pb2.SendOtpResponse()
        try:
            res = await Auth.sendOtp(request.identifier, request.type)
            response.ok = True
            return response
        except ProblemsWithRedisException:
            await context.abort(ProblemsWithRedisException.grpc_status, "Redis Error")
        except UserAlreadyExistsException:
            await context.abort(UserAlreadyExistsException.grpc_status, "User already exists")
        except Exception as e:
            # await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong...")
            await context.abort(grpc.StatusCode.INTERNAL, str(e))
        
    

    async def VerifyOtp(self, request, context):
        """
        request.identifier
        request.type       ["phone" | "email"]
        request.code
        """
        response = auth_pb2.VerifyOtpResponse()

        try:
            res : dict[str, str] = await Auth.verifyOtp(request.identifier, request.type, request.code)
        except IncorrectCodeException:
            await context.abort(IncorrectCodeException.grpc_status, "Incorrect code")
        except CodeNotFoundException:
            await context.abort(CodeNotFoundException.grpc_status, "Code was not found")
        except Exception:
            await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong...")

        response.access_token = res["access_token"]
        response.refresh_token = res["refresh_token"]
        return response
    
    async def Refresh(self, request, context):
        """
        request.refresh_token -> {access_token, refresh_token}
        """
        response = auth_pb2.RefreshResponse()
        try:
            res : dict[str, str] = await Auth.refresh(request.refresh_token)
            response.access_token = res["access_token"]
            response.refresh_token = res["refresh_token"]
            return response
        except TokenException as e:
            await context.abort(e.grpc_status, e.message)
        except Exception:
            await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong...")
        
