import database_pb2
import database_pb2_grpc


class DatabaseServiceServicer(database_pb2_grpc.DatabaseServiceServicer):
    def __init__(self):
        self.users = set()

    def CheckUserExists(self, request, context):
        username = request.username
        exists = username in self.users

        if not exists:
            self.users.add(username)

        return database_pb2.CheckUserResponse(exists=exists)
