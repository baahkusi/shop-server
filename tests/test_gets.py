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


def test_get_users(client):

    payload = {
        "111": {
            "get_users": {},
            "000": ["get_users"]
        },
        "000": ["111"]
    }

    login = Logins.select().order_by(Logins.id.desc()).get()

    headers = {
        'Authorization': login.token,
        'Account-ID': login.user.email,
        'Device-ID': login.device_hash
    }
    response = client.simulate_post('/action', body=json.dumps(payload), headers=headers)

    assert response.json["111"]["get_users"]["status"]

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


def test_fetch_combo(client):

    payload = {
        "111":{
            "fetch_combo":{"id":3},
            "000":["fetch_combo"]
        },
        "000":["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))

    assert response.json["111"]["fetch_combo"]["status"]


def test_get_combos(client):

    payload = {
        "111":{
            "get_combos":{
                "limit":4,
                "page":1
            },
            "000":["get_combos"]
        },
        "000":["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))

    assert response.json["111"]["get_combos"]["status"]


def test_get_combos_fetch(client):

    payload = {
        "111":{
            "get_combos":{
                "fetch":True,
                "user":2,
                "limit":4,
                "page":1
            },
            "000":["get_combos"]
        },
        "000":["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))
    assert response.json["111"]["get_combos"]["status"]


def test_get_combos_light(client):

    payload = {
        "111":{
            "get_combos":{
                "light":True,
                "user":2,
            },
            "000":["get_combos"]
        },
        "000":["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))
    assert response.json["111"]["get_combos"]["status"]