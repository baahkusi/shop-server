import json
from datauri import DataURI
from shop40.db import Logins, Users


def test_get_items(client):

    

    payload = {
        "111": {
            "get_items": {"limit":4},
            "000": ["get_items"]
        },
        "000": ["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))

    assert response.json["111"]["get_items"]["status"]
