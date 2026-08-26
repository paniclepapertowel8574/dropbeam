import pytest
from fastapi.testclient import TestClient

import app.config as app_config
from app import registry
from app.main import app

app_config.settings.scheduler_enabled = False


@pytest.fixture(autouse=True)
def clean_state():
    registry.clients.clear()
    registry.sockets.clear()
    registry.transfers.clear()
    yield
    registry.cleanup_expired()


@pytest.fixture()
def client():
    return TestClient(app)


def register(client, ua="TestAgent Chrome/120"):
    response = client.post("/api/register", headers={"user-agent": ua})
    assert response.status_code == 200
    return response.json()


def connect_ws(client, client_id):
    return client.websocket_connect(f"/ws?id={client_id}")
