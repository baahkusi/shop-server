from shop40.decors import login_required
from shop40.db import Logins, Users
import json


def test_decors(client):

    payload = {
        "111": {
            "decor_tester": {},
            "000": ["decor_tester"]
        },

        "000": ["111"]
    }

    login = Logins.select(Logins.token).join(Users).where(
        Users.email == 'usebaku@gmail.com').order_by(Logins.id.desc()).get()

    headers = {'Authorization': login.token}

    response = client.simulate_post(
        '/action', body=json.dumps(payload), headers=headers)
    print(response.json)
    assert response.json["111"]["decor_tester"]["status"]
    assert 0
