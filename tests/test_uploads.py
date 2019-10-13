import json
from datauri import DataURI
from shop40.db import Logins, Users


def test_upload_images(client):

    img1 = DataURI.from_file('tests/images/11.jpg')
    img2 = DataURI.from_file('tests/images/7.jpg')

    payload = {
        "111": {
            "upload_images": {
                'images': [{
                    'image': DataURI.from_file(f'tests/images/{i}.jpg'),
                    'tags': [f'img{i}']
                } for i in range(1, 17)]
            },
            "000": ["upload_images"]
        },
        "000": ["111"]
    }

    login = Logins.select(Logins.token).join(Users).order_by(
        Logins.id.desc()).get()

    headers = {'Authorization': login.token}

    response = client.simulate_post('/action',
                                    body=json.dumps(payload),
                                    headers=headers)
    assert response.json["111"]["upload_images"]["status"]
