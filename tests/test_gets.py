import json
from datauri import DataURI
from shop40.db import Logins, Users


def test_get_items(client):

    

    payload = {
        "111": {
            "get_items": {"page":1, "limit":16},
            "000": ["get_items"]
        },
        "000": ["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))

    assert response.json["111"]["get_items"]["status"]


def test_fetch_item(client):

    

    payload = {
        "111": {
            "fetch_item": {"item":1},
            "000": ["fetch_item"]
        },
        "000": ["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))

    assert response.json["111"]["fetch_item"]["status"]


def test_get_user(client):

    payload = {
        "111": {
            "get_user": {"id":1},
            "000": ["get_user"]
        },
        "000": ["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))

    assert response.json["111"]["get_user"]["status"]
