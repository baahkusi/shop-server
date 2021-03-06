import json
from shop40.db import Logins, Users


def test_get_items(client):

    info = {
        "name": "sbk",
        "address": "sbk",
        "phone": "553339728",
        "birth": "1995-03-20",
        "country": ["Ghana", "Ashanti"],
        "city": "Kumasi",
        "code": "+233",
    }

    payload = {
        "111": {
            "set_info": {
                "info": "personal",
                "data": info
            },
            "000": ["set_info"]
        },
        "000": ["111"]
    }

    login = Logins.select().order_by(Logins.id.desc()).get()

    headers = {
        'Authorization': login.token,
        'Account-ID': login.user.email,
        'Device-ID': login.device_hash
    }

    response = client.simulate_post('/action',
                                    body=json.dumps(payload),
                                    headers=headers)

    assert response.json["111"]["set_info"]["status"]


def test_like(client, auth_headers):

    payload = {
        "111": {
            "like": {
                "what": "combo",
                "pk": 1
            },
            "000": ["like"]
        },
        "000": ["111"]
    }

    response = client.simulate_post('/action',
                                    body=json.dumps(payload),
                                    headers=auth_headers)

    assert response.json["111"]["like"]["status"]
