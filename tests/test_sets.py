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
            "set_info": {"info":"personal", "data":info},
            "000": ["set_info"]
        },
        "000": ["111"]
    }

    login = Logins.select(Logins.token).order_by(Logins.id.desc()).get()

    headers = {'Authorization': login.token}

    response = client.simulate_post('/action',
                                    body=json.dumps(payload),
                                    headers=headers)

    assert response.json["111"]["set_info"]["status"]
