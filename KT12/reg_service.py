import grpc
import registration_pb2
import registration_pb2_grpc
import database_pb2


class RegistrationServiceServicer(registration_pb2_grpc.RegistrationServiceServicer):
    def __init__(self, database_stub):
        self.database_stub = database_stub

    def RegisterUser(self, request, context):
        username = request.username

        if not username:
            return registration_pb2.RegisterResponse(success=False, message="Username is required")

        check_request = database_pb2.CheckUserRequest(username=username)
        try:
            response = self.database_stub.CheckUserExists(check_request)

            if response.exists:
                return registration_pb2.RegisterResponse(success=False, message="User already exists")
            else:
                return registration_pb2.RegisterResponse(success=True, message="User registered successfully")
        except grpc.RpcError as e:
            return registration_pb2.RegisterResponse(success=False, message=f"Database error: {e}")
