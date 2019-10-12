import falcon
from falcon import testing
import pytest
from shop40.app import api


@pytest.fixture
def client():
    return testing.TestClient(api)
