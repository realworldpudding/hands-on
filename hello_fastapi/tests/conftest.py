from typing import Generator

from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient

from pudding_todo.app import create_app


@pytest.fixture(autouse=True)
def fastapi_app() -> Generator[FastAPI, None, None]:
    app = create_app()
    yield app


@pytest.fixture()
def client(fastapi_app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(fastapi_app) as test_client:
        yield test_client
