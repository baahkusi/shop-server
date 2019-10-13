import json
from datauri import DataURI
from shop40.db import Logins, Users


def test_upload_images(client):

    img1 = DataURI.from_file('tests/images/1.jpg')
    img2 = DataURI.from_file('tests/images/2.jpg')

    payload = {
        "111": {
            "upload_images": {'images':[img1, img2]},
            "000": ["upload_images"]
        },

        "000": ["111"]
    }


    login = Logins.select(Logins.token).join(Users).where(
        Users.email == 'usebaku@gmail.com').order_by(Logins.id.desc()).get()

    headers = {'Authorization': login.token}

    response = client.simulate_post(
        '/action', body=json.dumps(payload), headers=headers)
    print(response.json)
    assert response.json["111"]["upload_images"]["status"]
    assert 0
