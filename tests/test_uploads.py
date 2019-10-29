import json
from datauri import DataURI
from shop40.db import Logins, Users


def test_upload_item(client):

    imgs1 = [DataURI.from_file(f'tests/images/{i}.jpg') for i in range(1, 3)]
    imgs2 = [DataURI.from_file(f'tests/images/{i}.jpg') for i in range(7, 9)]
    imgs3 = [DataURI.from_file(f'tests/images/{i}.jpg') for i in range(13, 15)]

    item = {
        "category":1,
        "currency":"GHS",
        "images":imgs1,
        "tags": ["1", "2", "3", "4"],
        "options": [{
            "name": "opt1",
            "required":True,
            "values": [{
                "images": imgs2,
            }, {
                "images": imgs3,
            }]
        }]
    }

    payload = {
        "111": {
            "upload_item": {
                "item_details": item,
                "seller_id":1
            },
            "000": ["upload_item"]
        },
        "000": ["111"]
    }

    login = Logins.select(Logins.token).order_by(Logins.id.desc()).get()

    headers = {'Authorization': login.token}

    response = client.simulate_post('/action',
                                    body=json.dumps(payload),
                                    headers=headers)
    assert response.json["111"]["upload_item"]["status"]
