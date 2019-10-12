import falcon
from falcon import testing
import pytest
import json
from shop40.app import api


@pytest.fixture
def client():
    return testing.TestClient(api)


def test_register(client):
    payload = {
        "111": {
            "register": {"email":"sbksoftwares@gmail.com","password":"3229411841"},
            "000": ["register"]
        },

        "000": ["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))
    assert response.json["111"]["register"]["status"]



def test_login(client):
    payload = {
        "111": {
            "login": {
                "email":"sbksoftwares@gmail.com",
                "password":"3229411841",
                "device_hash":4636326,
                "device_data":{"user_agent":"Mozilla"}
                },
            "000": ["login"]
        },

        "000": ["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))
    
    assert response.json["111"]["login"]["status"]




















