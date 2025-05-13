import pytest
import grpc
import registration_pb2
import registration_pb2_grpc
import database_pb2
import database_pb2_grpc
from concurrent import futures
from db_service import DatabaseServiceServicer
from reg_service import RegistrationServiceServicer


def create_channel(host, port):
    return grpc.insecure_channel(f"{host}:{port}")


@pytest.fixture(scope="session")
def database_service():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    database_pb2_grpc.add_DatabaseServiceServicer_to_server(DatabaseServiceServicer(), server)

    server.add_insecure_port("[::]:50051")
    server.start()
    yield server
    server.stop(grace=None)


@pytest.fixture(scope="session")
def registration_service(database_service):
    channel = create_channel("localhost", 50051)
    database_stub = database_pb2_grpc.DatabaseServiceStub(channel)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registration_pb2_grpc.add_RegistrationServiceServicer_to_server(RegistrationServiceServicer(database_stub), server)

    server.add_insecure_port("[::]:50052")
    server.start()
    yield server
    server.stop(grace=None)


def test_registration(registration_service):
    channel = create_channel("localhost", 50052)
    stub = registration_pb2_grpc.RegistrationServiceStub(channel)
    request = registration_pb2.RegisterRequest(username="test", password="123")

    response = stub.RegisterUser(request)
    assert response.success


def test_registration_empty_username(registration_service):
    channel = create_channel("localhost", 50052)
    stub = registration_pb2_grpc.RegistrationServiceStub(channel)
    request = registration_pb2.RegisterRequest(username="", password="123")

    response = stub.RegisterUser(request)
    assert response.success is False


def test_registration_existing_user(database_service):
    channel = create_channel("localhost", 50051)
    stub = database_pb2_grpc.DatabaseServiceStub(channel)
    request = database_pb2.CheckUserRequest(username="test")

    response = stub.CheckUserExists(request)
    assert response.exists


def test_registration_non_existing_user(database_service):
    channel = create_channel("localhost", 50051)
    stub = database_pb2_grpc.DatabaseServiceStub(channel)
    request = database_pb2.CheckUserRequest(username="idontexist")
    response = stub.CheckUserExists(request)
    assert response.exists is False


def test_integration(registration_service, database_service):
    channel_db = create_channel("localhost", 50051)
    db_stub = database_pb2_grpc.DatabaseServiceStub(channel_db)
    db_request = database_pb2.CheckUserRequest(username="test")
    db_stub.CheckUserExists(db_request)

    channel_reg = create_channel("localhost", 50052)
    reg_stub = registration_pb2_grpc.RegistrationServiceStub(channel_reg)
    reg_request = registration_pb2.RegisterRequest(username="test", password="123")

    response = reg_stub.RegisterUser(reg_request)
    assert response.success is False
