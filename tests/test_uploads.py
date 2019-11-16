import json
from datauri import DataURI
from shop40.db import Logins, Users, Items


def test_upload_item(client):

    # test create
    imgs1 = [DataURI.from_file(f'tests/images/{i}.jpg') for i in range(1, 2)]
    imgs2 = [DataURI.from_file(f'tests/images/{i}.jpg') for i in range(7, 8)]
    imgs3 = [DataURI.from_file(f'tests/images/{i}.jpg') for i in range(13, 14)]

    item = {
        "category":
        1,
        "currency":
        "GHS",
        "images":
        imgs1,
        "tags": ["1", "2", "3", "4"],
        "options": [{
            "name": "opt1",
            "required": True,
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
                "seller_id": 1
            },
            "000": ["upload_item"]
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

    assert response.json["111"]["upload_item"]["status"]


def test_update_item(client):

    # test update
    imgs1 = [DataURI.from_file(f'tests/images/{i}.jpg') for i in range(3, 5)]
    imgs2 = [DataURI.from_file(f'tests/images/{i}.jpg') for i in range(9, 11)]
    imgs3 = [DataURI.from_file(f'tests/images/{i}.jpg') for i in range(15, 16)]

    item = {
        "category":
        2,
        "currency":
        "GHS",
        "images":
        imgs1,
        "tags": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        "options": [{
            "name": "opt1",
            "required": True,
            "values": [{
                "images": imgs2,
            }, {
                "images": imgs3,
            }]
        }]
    }

    item_new = Items.select(Items.id).order_by(Items.id.desc()).get()

    payload = {
        "111": {
            "upload_item": {
                "item_details": item,
                "seller_id": 1,
                "update": True,
                "id": item_new.id
            },
            "000": ["upload_item"]
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

    assert response.json["111"]["upload_item"]["status"]
