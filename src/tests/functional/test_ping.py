import json

def test_ping(test_app):
    ''' test rest api. '''

    print("Given")
    client = test_app.test_client()

    print("When")
    resp = client.get('/ping')
    data = json.loads(resp.data.decode())

    print("Then")

    assert resp.status_code == 200
    assert 'pong' in data['message']
    assert 'success' in data['status']
