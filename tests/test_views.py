from conftest import app
import base64

def test_root(client):
    headers = {'Authorization': 'Basic ' +
               base64.b64encode("test:")}
    #assert client.get('/initialize', headers=headers).status_code == 200
    assert client.get('/about').status_code == 200
